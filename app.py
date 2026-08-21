import sys
import os
import random
import io
import pandas as pd
import numpy as np
import joblib

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression

# =========================================================
# PROJECT PATHS & MODULE SETUP
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

try:
    from db_connection import create_engine_connection
    HAS_DB_MODULE = True
except Exception:
    HAS_DB_MODULE = False


app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)


@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


# =========================================================
# SYNTHETIC DATA GENERATOR (FALLBACK)
# =========================================================

def generate_fallback_data():
    """Generates 1,000 realistic student records if MySQL is offline."""
    np.random.seed(42)
    random.seed(42)

    names = [
        "Rahul Sharma", "Rohan Verma", "Raj Patel", "Vivek Joshi", "Arjun Mehta",
        "Yash Shah", "Harsh Gupta", "Dev Trivedi", "Jay Solanki", "Krish Kumar",
        "Neha Singh", "Pooja Desai", "Riya Kapoor", "Sneha Rao", "Anjali Nair",
        "Kavya Patel", "Nisha Agarwal", "Simran Kaur", "Aarav Sharma", "Ananya Iyer"
    ]

    cities = ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Gandhinagar", "Mumbai", "Delhi", "Pune"]
    genders = ["Male", "Female"]

    records = []
    for i in range(1, 1001):
        is_pass = random.random() < 0.81
        name = random.choice(names) + f" ({i})"
        age = random.randint(18, 24)
        gender = random.choice(genders)
        city = random.choice(cities)

        if not is_pass:
            attendance = round(random.uniform(40.0, 69.9), 2)
            study_hours = round(random.uniform(0.5, 2.5), 2)
            assignment_score = random.randint(20, 55)
            midterm_score = random.randint(20, 55)
            previous_score = random.randint(20, 55)
        else:
            attendance = round(random.uniform(70.0, 100.0), 2)
            study_hours = round(random.uniform(3.0, 8.5), 2)
            assignment_score = random.randint(55, 100)
            midterm_score = random.randint(50, 100)
            previous_score = random.randint(50, 100)

        final_score = (
            attendance * 0.20 +
            study_hours * 2.0 +
            assignment_score * 0.25 +
            midterm_score * 0.30 +
            previous_score * 0.15 +
            random.uniform(-4, 4)
        )
        final_score = round(max(0, min(100, final_score)), 2)

        records.append({
            "student_id": i,
            "name": name,
            "age": age,
            "gender": gender,
            "city": city,
            "attendance": attendance,
            "study_hours": study_hours,
            "assignment_score": assignment_score,
            "midterm_score": midterm_score,
            "previous_score": previous_score,
            "final_score": final_score
        })

    return pd.DataFrame(records)


# =========================================================
# DATA & MODEL LOADERS
# =========================================================

def load_data():
    """Load dataset from MySQL DB or fallback to synthetic data gracefully."""
    if HAS_DB_MODULE:
        try:
            engine = create_engine_connection()
            query = """
            SELECT
                s.student_id,
                s.name,
                s.age,
                s.gender,
                s.city,
                p.attendance,
                p.study_hours,
                p.assignment_score,
                p.midterm_score,
                p.previous_score,
                p.final_score
            FROM students s
            INNER JOIN performance p
            ON s.student_id = p.student_id
            """
            df_sql = pd.read_sql(query, engine)
            if not df_sql.empty:
                return df_sql, True
        except Exception:
            pass

    return generate_fallback_data(), False


def load_ml_models(df_data):
    """Load trained models or train dynamic fallbacks if PKL files are missing."""
    score_model = None
    classification_model = None

    reg_path = os.path.join(BASE_DIR, "models", "student_score_model.pkl")
    clf_path = os.path.join(BASE_DIR, "models", "best_pass_fail_model.pkl")

    if os.path.exists(reg_path):
        try:
            score_model = joblib.load(reg_path)
        except Exception:
            score_model = None

    if os.path.exists(clf_path):
        try:
            classification_model = joblib.load(clf_path)
        except Exception:
            classification_model = None

    features = ["attendance", "study_hours", "assignment_score", "midterm_score", "previous_score"]

    if score_model is None:
        X = df_data[features]
        y_score = df_data["final_score"]
        score_model = RandomForestRegressor(n_estimators=100, random_state=42)
        score_model.fit(X, y_score)

    if classification_model is None:
        X = df_data[features]
        y_class = (df_data["final_score"] >= 40).astype(int)
        classification_model = RandomForestClassifier(n_estimators=100, random_state=42)
        classification_model.fit(X, y_class)

    return score_model, classification_model


# Initialize dataset & ML models
df_raw, IS_DB_CONNECTED = load_data()
df_raw["result"] = df_raw["final_score"].apply(lambda x: "PASS" if x >= 40 else "FAIL")
SCORE_MODEL, CLASSIFICATION_MODEL = load_ml_models(df_raw)


# =========================================================
# ROUTES
# =========================================================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/meta", methods=["GET"])
def get_meta():
    """Return dropdown options and min/max ranges for global filters."""
    all_cities = sorted(df_raw["city"].unique().tolist())
    all_genders = sorted(df_raw["gender"].unique().tolist())
    min_age = int(df_raw["age"].min())
    max_age = int(df_raw["age"].max())

    return jsonify({
        "cities": all_cities,
        "genders": all_genders,
        "min_age": min_age,
        "max_age": max_age,
        "is_db_connected": IS_DB_CONNECTED
    })


@app.route("/api/data", methods=["POST"])
def get_data():
    """API endpoint to fetch metrics, chart data, and student list based on filters."""
    params = request.get_json() or {}

    selected_cities = params.get("cities", [])
    selected_genders = params.get("genders", [])
    age_min = params.get("age_min")
    age_max = params.get("age_max")
    result_filter = params.get("result_filter", "All")

    df_filtered = df_raw.copy()

    if selected_cities:
        df_filtered = df_filtered[df_filtered["city"].isin(selected_cities)]

    if selected_genders:
        df_filtered = df_filtered[df_filtered["gender"].isin(selected_genders)]

    if age_min is not None and age_max is not None:
        df_filtered = df_filtered[(df_filtered["age"] >= age_min) & (df_filtered["age"] <= age_max)]

    if result_filter == "PASS Only":
        df_filtered = df_filtered[df_filtered["result"] == "PASS"]
    elif result_filter == "FAIL Only":
        df_filtered = df_filtered[df_filtered["result"] == "FAIL"]

    total_count = len(df_filtered)
    if total_count == 0:
        return jsonify({
            "empty": True,
            "message": "No student records match the current filter criteria."
        })

    avg_score = round(float(df_filtered["final_score"].mean()), 2)
    passed_count = int((df_filtered["result"] == "PASS").sum())
    failed_count = int((df_filtered["result"] == "FAIL").sum())
    pass_pct = round((passed_count / total_count * 100), 1)
    fail_pct = round((failed_count / total_count * 100), 1)

    top_city_row = (
        df_filtered.groupby("city")["final_score"]
        .mean()
        .reset_index()
        .sort_values("final_score", ascending=False)
    )
    top_city = top_city_row.iloc[0]["city"] if not top_city_row.empty else "N/A"
    top_city_score = round(float(top_city_row.iloc[0]["final_score"]), 1) if not top_city_row.empty else 0

    # City-wise stats for bar chart
    city_stats = (
        df_filtered.groupby("city")
        .agg(
            avg_score=("final_score", "mean"),
            student_count=("student_id", "count"),
            pass_rate=("result", lambda x: (x == "PASS").mean() * 100)
        )
        .reset_index()
        .sort_values("avg_score", ascending=False)
    )
    city_stats["avg_score"] = city_stats["avg_score"].round(1)
    city_stats["pass_rate"] = city_stats["pass_rate"].round(1)

    # Feature Importance computation
    features = ["attendance", "study_hours", "assignment_score", "midterm_score", "previous_score"]
    feature_names = ["Attendance (%)", "Study Hours (hrs)", "Assignment Score", "Midterm Score", "Previous Score"]
    
    reg_importances = list(getattr(SCORE_MODEL, "feature_importances_", [0.2]*5))
    clf_importances = list(getattr(CLASSIFICATION_MODEL, "feature_importances_", [0.2]*5))

    feature_imp_data = []
    for fn, r_imp, c_imp in zip(feature_names, reg_importances, clf_importances):
        feature_imp_data.append({
            "feature": fn,
            "score_importance": round(float(r_imp * 100), 1),
            "class_importance": round(float(c_imp * 100), 1)
        })

    # Correlation Matrix
    corr_features = ["attendance", "study_hours", "assignment_score", "midterm_score", "previous_score", "final_score"]
    corr_matrix = df_filtered[corr_features].corr().round(2).to_dict()

    # Scatter sampling (up to 300 points for speed)
    sample_df = df_filtered.sample(min(300, len(df_filtered)), random_state=42)
    attendance_scatter = sample_df[["attendance", "final_score", "result", "name"]].to_dict(orient="records")
    study_hours_scatter = sample_df[["study_hours", "final_score", "result", "name"]].to_dict(orient="records")

    students_list = df_filtered.to_dict(orient="records")

    return jsonify({
        "empty": False,
        "summary": {
            "total_count": total_count,
            "avg_score": avg_score,
            "passed_count": passed_count,
            "failed_count": failed_count,
            "pass_pct": pass_pct,
            "fail_pct": fail_pct,
            "top_city": top_city,
            "top_city_score": top_city_score,
            "is_db_connected": IS_DB_CONNECTED
        },
        "charts": {
            "pass_fail": {"PASS": passed_count, "FAIL": failed_count},
            "city_stats": city_stats.to_dict(orient="records"),
            "feature_importances": feature_imp_data,
            "correlation": corr_matrix,
            "attendance_scatter": attendance_scatter,
            "study_hours_scatter": study_hours_scatter
        },
        "students": students_list
    })


@app.route("/api/predict", methods=["POST"])
def predict():
    """Predict final score and Pass/Fail status with probability and advice."""
    data = request.get_json() or {}

    try:
        attendance = float(data.get("attendance", 75))
        study_hours = float(data.get("study_hours", 4.0))
        assignment_score = float(data.get("assignment_score", 70))
        midterm_score = float(data.get("midterm_score", 65))
        previous_score = float(data.get("previous_score", 65))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input numbers provided."}), 400

    input_df = pd.DataFrame([{
        "attendance": attendance,
        "study_hours": study_hours,
        "assignment_score": assignment_score,
        "midterm_score": midterm_score,
        "previous_score": previous_score
    }])

    pred_score = float(SCORE_MODEL.predict(input_df)[0])
    pred_score = max(0.0, min(100.0, pred_score))

    pred_class = int(CLASSIFICATION_MODEL.predict(input_df)[0])
    result_str = "PASS" if pred_class == 1 else "FAIL"

    if hasattr(CLASSIFICATION_MODEL, "predict_proba"):
        probs = CLASSIFICATION_MODEL.predict_proba(input_df)[0]
        fail_prob = round(float(probs[0] * 100), 1)
        pass_prob = round(float(probs[1] * 100), 1)
    else:
        pass_prob = 100.0 if pred_class == 1 else 0.0
        fail_prob = 100.0 - pass_prob

    # Generate personalized recommendations
    recommendations = []
    if attendance < 75:
        recommendations.append("⚠️ **Attendance Alert**: Attendance is below 75%. Aim for at least 80% to ensure key concepts are not missed.")
    if study_hours < 3.0:
        recommendations.append("📚 **Study Habit**: Daily study time is low. Incrementally boost study hours to 3.5–5 hours/day.")
    if assignment_score < 60:
        recommendations.append("📝 **Assignment Boost**: Assignment score is low. Review feedback on previous assignments and seek assistance.")
    if midterm_score < 50:
        recommendations.append("🎯 **Midterm Recovery**: Focus revision on weak topics identified in midterms prior to final exams.")

    if not recommendations:
        recommendations.append("🌟 **Excellent Profile**: Academic habits are strong across all tracked metrics. Keep up the consistent effort!")

    advice_text = " ".join(recommendations)

    return jsonify({
        "predicted_score": round(pred_score, 1),
        "result": result_str,
        "pass_probability": pass_prob,
        "fail_probability": fail_prob,
        "advice": advice_text,
        "inputs": {
            "attendance": attendance,
            "study_hours": study_hours,
            "assignment_score": assignment_score,
            "midterm_score": midterm_score,
            "previous_score": previous_score
        }
    })


@app.route("/api/sql", methods=["POST"])
def execute_sql():
    """Run prepackaged query or custom SELECT query against DataFrame or SQL."""
    data = request.get_json() or {}
    query_type = data.get("query_type")

    if query_type == "top_performers":
        res_df = df_raw.sort_values("final_score", ascending=False).head(10)
        title = "Top 10 High Performing Students"
    elif query_type == "at_risk":
        res_df = df_raw[df_raw["final_score"] < 40].sort_values("final_score", ascending=True).head(10)
        title = "Top 10 At-Risk Students (Score < 40)"
    elif query_type == "city_avg":
        res_df = df_raw.groupby("city").agg(
            total_students=("student_id", "count"),
            avg_final_score=("final_score", "mean"),
            avg_attendance=("attendance", "mean")
        ).round(2).reset_index().sort_values("avg_final_score", ascending=False)
        title = "City-wise Academic Breakdown"
    else:
        return jsonify({"error": "Invalid analytical query selection."}), 400

    columns = res_df.columns.tolist()
    rows = res_df.to_dict(orient="records")

    return jsonify({
        "title": title,
        "columns": columns,
        "rows": rows,
        "row_count": len(rows)
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    try:
        from waitress import serve
        print(f"Serving StudentIQ Production WSGI Server (Waitress) on http://0.0.0.0:{port}")
        serve(app, host="0.0.0.0", port=port)
    except ImportError:
        print(f"Starting StudentIQ Flask Web Server on http://0.0.0.0:{port}")
        app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)