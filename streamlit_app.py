import sys
import os
import random
import io

# =========================================================
# PROJECT PATHS & MODULE SETUP
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


# =========================================================
# IMPORTS
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go

from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression

try:
    from db_connection import create_engine_connection
    HAS_DB_MODULE = True
except Exception:
    HAS_DB_MODULE = False


# =========================================================
# STREAMLIT PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="StudentIQ • Academic Intelligence Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS SYSTEM (FUTURISTIC DARK GLASSMORPHISM)
# =========================================================

st.markdown(
    """
    <style>
    /* Main Background & Global Text */
    .stApp {
        background-color: #070a13;
        color: #f1f5f9;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    /* Hide standard header & footer */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0b0f19 !important;
        border-right: 1px solid #1e293b !important;
    }

    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] label {
        color: #e2e8f0 !important;
    }

    /* Sidebar Caption Header Text */
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p,
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: #94a3b8 !important;
        font-size: 12px !important;
        font-weight: 800 !important;
        letter-spacing: 0.8px !important;
        text-transform: uppercase !important;
    }

    .brand-container {
        padding: 10px 0 15px 0;
        text-align: center;
    }

    .brand-title {
        font-size: 26px;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }

    .brand-sub {
        color: #64748b !important;
        font-size: 12px;
        font-weight: 600;
        margin-top: 2px;
    }

    /* Custom Navigation Radio Buttons */
    div[data-testid="stSidebarUserContent"] .stRadio label {
        background: #111827 !important;
        border: 1px solid #1f2937 !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        margin-bottom: 6px !important;
        transition: all 0.2s ease-in-out;
    }

    div[data-testid="stSidebarUserContent"] .stRadio label p {
        color: #f1f5f9 !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        text-transform: none !important;
        letter-spacing: 0 !important;
    }

    div[data-testid="stSidebarUserContent"] .stRadio label:hover {
        border-color: #6366f1 !important;
        background: #1e1b4b !important;
    }

    /* Header Banner */
    .hero-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 25px;
        padding-bottom: 15px;
        border-bottom: 1px solid #1e293b;
    }

    .page-title {
        font-size: 32px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.5px;
        margin: 0;
    }

    .page-subtitle {
        color: #94a3b8;
        font-size: 14px;
        margin-top: 4px;
    }

    .status-badge-live {
        background-color: rgba(16, 185, 129, 0.15);
        border: 1px solid #10b981;
        color: #34d399;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    .status-badge-offline {
        background-color: rgba(245, 158, 11, 0.15);
        border: 1px solid #f59e0b;
        color: #fbbf24;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(145deg, #0f172a 0%, #131c31 100%);
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: #6366f1;
    }

    .kpi-label {
        color: #94a3b8;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .kpi-value {
        color: #ffffff;
        font-size: 32px;
        font-weight: 800;
        margin: 8px 0 4px 0;
    }

    .kpi-footer {
        color: #38bdf8;
        font-size: 12px;
        font-weight: 500;
    }

    /* Custom Glass Containers */
    .glass-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
    }

    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Styled Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: none;
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: #ffffff;
        font-weight: 700;
        padding: 12px 20px;
        font-size: 15px;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4);
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6);
        color: #ffffff;
    }

    /* AI Advice Card */
    .advice-card {
        background: linear-gradient(145deg, #1e1b4b 0%, #0f172a 100%);
        border: 1px solid #6366f1;
        border-radius: 16px;
        padding: 20px;
        margin-top: 15px;
    }

    .advice-title {
        color: #a5b4fc;
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .advice-body {
        color: #e0e7ff;
        font-size: 14px;
        line-height: 1.5;
    }

    /* Footer */
    .custom-footer {
        text-align: center;
        color: #64748b;
        font-size: 12px;
        padding: 25px 0 10px 0;
        border-top: 1px solid #1e293b;
        margin-top: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SYNTHETIC DATA GENERATOR (RESILIENT FALLBACK)
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
# DATA & MODEL LOADERS WITH CACHING
# =========================================================

@st.cache_data
def load_data():
    """Load dataset from MySQL DB or fallback to synthetic data gracefully."""
    db_status = False
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

    # Fallback if DB connection fails
    return generate_fallback_data(), False


@st.cache_resource
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

    # Fallback training if pkl unavailable
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


# =========================================================
# INITIALIZE DATA & MODELS
# =========================================================

df_raw, is_db_connected = load_data()

# Compute result column
df_raw["result"] = df_raw["final_score"].apply(lambda x: "PASS" if x >= 40 else "FAIL")

score_model, classification_model = load_ml_models(df_raw)


# =========================================================
# SIDEBAR CONTROLS & FILTERS
# =========================================================

with st.sidebar:
    st.markdown(
        """
        <div class="brand-container">
            <div class="brand-title">🎓 StudentIQ</div>
            <div class="brand-sub">Academic Intelligence & Prediction</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.caption("MAIN NAVIGATION")

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📊 Analytics",
            "🤖 AI Prediction",
            "🔍 Student Search",
            "🗄️ SQL Insights"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.caption("GLOBAL FILTERS")

    all_cities = sorted(df_raw["city"].unique().tolist())
    selected_cities = st.multiselect("Select City", all_cities, default=all_cities)

    all_genders = sorted(df_raw["gender"].unique().tolist())
    selected_genders = st.multiselect("Select Gender", all_genders, default=all_genders)

    min_age = int(df_raw["age"].min())
    max_age = int(df_raw["age"].max())
    age_range = st.slider("Age Range", min_age, max_age, (min_age, max_age))

    result_filter = st.radio("Result Status", ["All", "PASS Only", "FAIL Only"])

    st.divider()

    st.caption("SYSTEM STATUS")

    if is_db_connected:
        st.success("🟢 MySQL Connected")
    else:
        st.warning("🟠 Offline Mode (Sample Data)")

    st.success("🟢 ML Models Active")

    st.divider()

    st.caption("StudentIQ v2.0 • Streamlit 1.61+")
    st.caption("Python • SQL • Scikit-Learn • Plotly")


# =========================================================
# APPLY GLOBAL FILTERS TO DATAFRAME
# =========================================================

df_filtered = df_raw.copy()

if selected_cities:
    df_filtered = df_filtered[df_filtered["city"].isin(selected_cities)]

if selected_genders:
    df_filtered = df_filtered[df_filtered["gender"].isin(selected_genders)]

df_filtered = df_filtered[
    (df_filtered["age"] >= age_range[0]) & (df_filtered["age"] <= age_range[1])
]

if result_filter == "PASS Only":
    df_filtered = df_filtered[df_filtered["result"] == "PASS"]
elif result_filter == "FAIL Only":
    df_filtered = df_filtered[df_filtered["result"] == "FAIL"]


# =========================================================
# HELPER PLOTLY THEMING
# =========================================================

PLOTLY_DARK_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#94a3b8", family="Inter, sans-serif"),
    xaxis=dict(gridcolor="#1e293b", zerolinecolor="#1e293b", tickfont=dict(color="#cbd5e1")),
    yaxis=dict(gridcolor="#1e293b", zerolinecolor="#1e293b", tickfont=dict(color="#cbd5e1")),
    margin=dict(l=20, r=20, t=40, b=30)
)


# =========================================================
# PAGE 1: 🏠 DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    status_badge = (
        '<span class="status-badge-live">● LIVE MYSQL CONNECTED</span>'
        if is_db_connected else
        '<span class="status-badge-offline">● OFFLINE DATA MODE</span>'
    )

    st.markdown(
        f"""
        <div class="hero-header">
            <div>
                <div class="page-title">Student Performance Intelligence</div>
                <div class="page-subtitle">Real-time overview & KPI metrics of student academic standing</div>
            </div>
            <div>{status_badge}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if df_filtered.empty:
        st.warning("No records match the current sidebar filter parameters. Please widen your selection.")
        st.stop()

    # Metrics computation
    total_count = len(df_filtered)
    avg_score = df_filtered["final_score"].mean()
    passed_count = (df_filtered["result"] == "PASS").sum()
    failed_count = (df_filtered["result"] == "FAIL").sum()
    pass_pct = (passed_count / total_count * 100) if total_count > 0 else 0
    fail_pct = (failed_count / total_count * 100) if total_count > 0 else 0

    top_city_row = (
        df_filtered.groupby("city")["final_score"]
        .mean()
        .reset_index()
        .sort_values("final_score", ascending=False)
    )
    top_city_name = top_city_row.iloc[0]["city"] if not top_city_row.empty else "N/A"

    # KPI Row
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Total Students</div>
                <div class="kpi-value">{total_count:,}</div>
                <div class="kpi-footer">Filtered records</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Average Final Score</div>
                <div class="kpi-value">{avg_score:.2f}</div>
                <div class="kpi-footer">Out of 100 points</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Pass Rate</div>
                <div class="kpi-value" style="color: #34d399;">{pass_pct:.1f}%</div>
                <div class="kpi-footer">{passed_count:,} students passed</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">Top Performing City</div>
                <div class="kpi-value" style="color: #38bdf8;">{top_city_name}</div>
                <div class="kpi-footer">Highest avg score</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")
    st.write("")

    # Visual Charts Row
    left, right = st.columns([1.6, 1])

    with left:
        st.markdown('<div class="section-title">📊 City-wise Average Performance</div>', unsafe_allow_html=True)
        city_perf = (
            df_filtered.groupby("city")
            .agg(
                Student_Count=("student_id", "count"),
                Average_Score=("final_score", "mean")
            )
            .reset_index()
            .sort_values("Average_Score", ascending=True)
        )
        city_perf["Average_Score"] = city_perf["Average_Score"].round(2)

        fig_city = px.bar(
            city_perf,
            x="Average_Score",
            y="city",
            orientation="h",
            text="Average_Score",
            color="Average_Score",
            color_continuous_scale=["#312e81", "#6366f1", "#06b6d4"],
            labels={"Average_Score": "Average Score", "city": "City"}
        )
        fig_city.update_layout(**PLOTLY_DARK_LAYOUT, height=380, coloraxis_showscale=False)
        fig_city.update_traces(textposition="outside", texttemplate="%{text:.2f}")
        st.plotly_chart(fig_city)

    with right:
        st.markdown('<div class="section-title">📈 Pass vs Fail Ratio</div>', unsafe_allow_html=True)
        res_counts = df_filtered["result"].value_counts().reset_index()
        res_counts.columns = ["Result", "Count"]

        fig_pie = px.pie(
            res_counts,
            names="Result",
            values="Count",
            hole=0.55,
            color="Result",
            color_discrete_map={"PASS": "#10b981", "FAIL": "#f43f5e"}
        )
        fig_pie.update_layout(**PLOTLY_DARK_LAYOUT, height=380, showlegend=True)
        fig_pie.update_traces(textinfo="percent+label", pull=[0.05, 0.05])
        st.plotly_chart(fig_pie)

    st.markdown('<div class="section-title">🏆 Top Performing Cities Leaderboard</div>', unsafe_allow_html=True)
    city_leaderboard = (
        df_filtered.groupby("city")
        .agg(
            Total_Students=("student_id", "count"),
            Average_Score=("final_score", "mean"),
            Pass_Rate=("result", lambda x: f"{(x == 'PASS').sum() / len(x) * 100:.1f}%")
        )
        .reset_index()
        .sort_values("Average_Score", ascending=False)
    )
    city_leaderboard["Average_Score"] = city_leaderboard["Average_Score"].round(2)

    st.dataframe(city_leaderboard, hide_index=True)


# =========================================================
# PAGE 2: 📊 ANALYTICS
# =========================================================

elif page == "📊 Analytics":

    st.markdown(
        """
        <div class="hero-header">
            <div>
                <div class="page-title">Performance Analytics & Factor Correlation</div>
                <div class="page-subtitle">Deep dive into relationships between attendance, study hours, and exam scores</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if df_filtered.empty:
        st.warning("No records available to display analytics.")
        st.stop()

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-title">⏱️ Attendance vs Final Score</div>', unsafe_allow_html=True)
        fig_scatter1 = px.scatter(
            df_filtered,
            x="attendance",
            y="final_score",
            color="result",
            color_discrete_map={"PASS": "#10b981", "FAIL": "#f43f5e"},
            hover_data=["name", "study_hours"],
            labels={"attendance": "Attendance (%)", "final_score": "Final Score"}
        )
        fig_scatter1.update_layout(**PLOTLY_DARK_LAYOUT, height=380)
        st.plotly_chart(fig_scatter1)

    with c2:
        st.markdown('<div class="section-title">📚 Study Hours vs Final Score</div>', unsafe_allow_html=True)
        fig_scatter2 = px.scatter(
            df_filtered,
            x="study_hours",
            y="final_score",
            color="result",
            color_discrete_map={"PASS": "#10b981", "FAIL": "#f43f5e"},
            hover_data=["name", "attendance"],
            labels={"study_hours": "Daily Study Hours", "final_score": "Final Score"}
        )
        fig_scatter2.update_layout(**PLOTLY_DARK_LAYOUT, height=380)
        st.plotly_chart(fig_scatter2)

    c3, c4 = st.columns(2)

    with c3:
        st.markdown('<div class="section-title">🔗 Correlation Matrix Heatmap</div>', unsafe_allow_html=True)
        feature_cols = ["attendance", "study_hours", "assignment_score", "midterm_score", "previous_score", "final_score"]
        corr_matrix = df_filtered[feature_cols].corr().round(2)

        fig_heatmap = px.imshow(
            corr_matrix,
            text_auto=True,
            color_continuous_scale="Purples",
            aspect="auto"
        )
        fig_heatmap.update_layout(**PLOTLY_DARK_LAYOUT, height=380)
        st.plotly_chart(fig_heatmap)

    with c4:
        st.markdown('<div class="section-title">⭐ Feature Importance (RandomForest)</div>', unsafe_allow_html=True)
        features = ["attendance", "study_hours", "assignment_score", "midterm_score", "previous_score"]
        X_feat = df_raw[features]
        y_feat = df_raw["final_score"]

        rf_temp = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_temp.fit(X_feat, y_feat)

        imp_df = pd.DataFrame({
            "Feature": ["Attendance", "Study Hours", "Assignment", "Midterm", "Previous Score"],
            "Importance": rf_temp.feature_importances_
        }).sort_values("Importance", ascending=True)

        fig_imp = px.bar(
            imp_df,
            x="Importance",
            y="Feature",
            orientation="h",
            text="Importance",
            color="Importance",
            color_continuous_scale="Viridis"
        )
        fig_imp.update_layout(**PLOTLY_DARK_LAYOUT, height=380, coloraxis_showscale=False)
        fig_imp.update_traces(texttemplate="%{text:.3f}", textposition="outside")
        st.plotly_chart(fig_imp)


# =========================================================
# PAGE 3: 🤖 AI PREDICTION STUDIO
# =========================================================

elif page == "🤖 AI Prediction":

    st.markdown(
        """
        <div class="hero-header">
            <div>
                <div class="page-title">🤖 AI Performance Predictor Studio</div>
                <div class="page-subtitle">Predict final student scores and PASS / FAIL probability using machine learning</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(["🎯 Single Student Predictor", "📁 Batch Prediction (CSV Upload)"])

    with tab1:
        st.markdown('<div class="section-title">Input Student Parameters</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            attendance = st.slider("Attendance Rate (%)", 0.0, 100.0, 85.0, 0.5)
            study_hours = st.slider("Daily Study Hours", 0.0, 16.0, 4.5, 0.25)
            assignment_score = st.number_input("Assignment Score (0 - 100)", 0.0, 100.0, 78.0, 1.0)

        with col2:
            midterm_score = st.number_input("Midterm Exam Score (0 - 100)", 0.0, 100.0, 72.0, 1.0)
            previous_score = st.number_input("Previous Term Score (0 - 100)", 0.0, 100.0, 75.0, 1.0)

        predict_btn = st.button("✨ Predict Student Performance")

        if predict_btn:
            input_df = pd.DataFrame([{
                "attendance": attendance,
                "study_hours": study_hours,
                "assignment_score": assignment_score,
                "midterm_score": midterm_score,
                "previous_score": previous_score
            }])

            # Predict Score
            pred_score = score_model.predict(input_df)[0]
            pred_score = round(max(0, min(100, pred_score)), 2)

            # Predict Class & Probability
            pred_class = classification_model.predict(input_df)[0]
            pred_proba = classification_model.predict_proba(input_df)[0]

            pass_prob = round(pred_proba[1] * 100, 1) if len(pred_proba) > 1 else (100.0 if pred_class == 1 else 0.0)
            fail_prob = round(100.0 - pass_prob, 1)

            st.divider()

            res_c1, res_c2, res_c3 = st.columns(3)

            with res_c1:
                st.metric("Predicted Final Score", f"{pred_score:.2f} / 100")

            with res_c2:
                if pred_class == 1 or pred_score >= 40:
                    st.success("Result Status: PASS ✅")
                else:
                    st.error("Result Status: FAIL ❌")

            with res_c3:
                st.metric("Pass Confidence", f"{pass_prob:.1f}%")

            # Plotly Gauge Chart for Score
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=pred_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Predicted Final Score Gauge", 'font': {'color': "#ffffff", 'size': 18}},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': "#cbd5e1"},
                    'bar': {'color': "#6366f1"},
                    'steps': [
                        {'range': [0, 40], 'color': "rgba(244, 63, 94, 0.4)"},
                        {'range': [40, 70], 'color': "rgba(245, 158, 11, 0.4)"},
                        {'range': [70, 100], 'color': "rgba(16, 185, 129, 0.4)"}
                    ],
                }
            ))
            fig_gauge.update_layout(**PLOTLY_DARK_LAYOUT, height=280)
            st.plotly_chart(fig_gauge)

            # AI Academic Advice Logic
            advice_list = []
            if attendance < 75:
                advice_list.append("⚠️ **Critical Attendance Alert**: Attendance is under 75%. Increasing attendance above 80% can significantly improve overall final performance.")
            if study_hours < 3.0:
                advice_list.append("📚 **Study Hours Boost Recommended**: Increasing daily study time by 1 to 2 hours will help boost assignment and exam readiness.")
            if midterm_score < 50:
                advice_list.append("📝 **Exam Support Needed**: Midterm score is low. Focused revision on weak exam modules is recommended.")

            if not advice_list:
                advice_list.append("🌟 **Excellent Academic Trajectory**: The student demonstrates solid performance parameters across study hours, attendance, and exam scores!")

            advice_text = "<br>".join(advice_list)

            st.markdown(
                f"""
                <div class="advice-card">
                    <div class="advice-title">💡 Personalized AI Academic Recommendations</div>
                    <div class="advice-body">{advice_text}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with tab2:
        st.markdown('<div class="section-title">Upload CSV for Batch Prediction</div>', unsafe_allow_html=True)
        st.caption("CSV file must contain columns: `attendance`, `study_hours`, `assignment_score`, `midterm_score`, `previous_score`")

        uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

        if uploaded_file is not None:
            try:
                batch_df = pd.read_csv(uploaded_file)
                req_cols = ["attendance", "study_hours", "assignment_score", "midterm_score", "previous_score"]

                if all(col in batch_df.columns for col in req_cols):
                    batch_inputs = batch_df[req_cols]
                    batch_scores = score_model.predict(batch_inputs)
                    batch_classes = classification_model.predict(batch_inputs)

                    batch_df["Predicted_Final_Score"] = np.round(np.clip(batch_scores, 0, 100), 2)
                    batch_df["Predicted_Result"] = np.where(batch_classes == 1, "PASS", "FAIL")

                    st.success(f"Batch prediction completed for {len(batch_df)} rows!")
                    st.dataframe(batch_df, hide_index=True)

                    csv_buffer = io.StringIO()
                    batch_df.to_csv(csv_buffer, index=False)
                    st.download_button(
                        label="📥 Download Predictions CSV",
                        data=csv_buffer.getvalue(),
                        file_name="student_predictions.csv",
                        mime="text/csv"
                    )
                else:
                    st.error(f"Missing required columns in CSV! Expected: {req_cols}")
            except Exception as e:
                st.error(f"Error processing CSV file: {e}")


# =========================================================
# PAGE 4: 🔍 STUDENT SEARCH & PROFILE DEEP-DIVE
# =========================================================

elif page == "🔍 Student Search":

    st.markdown(
        """
        <div class="hero-header">
            <div>
                <div class="page-title">🔍 Student Directory & Search</div>
                <div class="page-subtitle">Search, filter, and inspect individual student scorecards and profiles</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    s1, s2 = st.columns([1, 2])

    with s1:
        search_type = st.selectbox("Search Filter", ["All Students", "Student ID", "Student Name", "City"])

    with s2:
        search_query = st.text_input("Enter Search Term", placeholder="e.g. Rahul, Ahmedabad, or 105")

    search_df = df_filtered.copy()

    if search_query.strip():
        if search_type == "Student ID" and search_query.strip().isdigit():
            search_df = search_df[search_df["student_id"] == int(search_query.strip())]
        elif search_type == "Student Name":
            search_df = search_df[search_df["name"].str.contains(search_query, case=False, na=False)]
        elif search_type == "City":
            search_df = search_df[search_df["city"].str.contains(search_query, case=False, na=False)]
        elif search_type == "All Students":
            search_df = search_df[
                search_df["name"].str.contains(search_query, case=False, na=False) |
                search_df["city"].str.contains(search_query, case=False, na=False) |
                search_df["student_id"].astype(str).str.contains(search_query, case=False, na=False)
            ]

    st.markdown(f"**Found {len(search_df):,} Record(s)**")
    st.dataframe(search_df, hide_index=True)

    # Export Button
    csv_search = io.StringIO()
    search_df.to_csv(csv_search, index=False)
    st.download_button("📥 Export Results to CSV", csv_search.getvalue(), "student_search_results.csv", "text/csv")

    st.divider()

    # Individual Profile Scorecard Modal/Deep Dive
    st.markdown('<div class="section-title">👤 Individual Student Performance Scorecard</div>', unsafe_allow_html=True)

    if not search_df.empty:
        student_options = search_df.apply(lambda r: f"ID #{r['student_id']} - {r['name']} ({r['city']})", axis=1).tolist()
        selected_student_str = st.selectbox("Select Student Profile to Inspect", student_options)

        if selected_student_str:
            selected_id = int(selected_student_str.split("ID #")[1].split(" -")[0])
            st_row = search_df[search_df["student_id"] == selected_id].iloc[0]

            sc1, sc2 = st.columns([1, 1.2])

            with sc1:
                st.markdown(
                    f"""
                    <div class="glass-card">
                        <h3 style="color: #ffffff; margin-bottom: 5px;">{st_row['name']}</h3>
                        <p style="color: #94a3b8; font-size: 13px;">Student ID: #{st_row['student_id']} | City: {st_row['city']} | Age: {st_row['age']} | Gender: {st_row['gender']}</p>
                        <hr style="border-color: #1e293b;">
                        <p><b>Attendance Rate:</b> {st_row['attendance']}%</p>
                        <p><b>Daily Study Hours:</b> {st_row['study_hours']} hrs</p>
                        <p><b>Assignment Score:</b> {st_row['assignment_score']} / 100</p>
                        <p><b>Midterm Exam Score:</b> {st_row['midterm_score']} / 100</p>
                        <p><b>Previous Term Score:</b> {st_row['previous_score']} / 100</p>
                        <p style="font-size: 18px; font-weight: 700; color: #ffffff;">Final Score: {st_row['final_score']} / 100</p>
                        <span class="{"status-badge-live" if st_row['result'] == 'PASS' else "status-badge-offline"}">{st_row['result']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with sc2:
                # Plotly Polar / Radar Chart for Student Scorecard
                categories = ['Attendance %', 'Assignment', 'Midterm', 'Previous Score', 'Final Score']
                values = [st_row['attendance'], st_row['assignment_score'], st_row['midterm_score'], st_row['previous_score'], st_row['final_score']]

                fig_radar = go.Figure()
                fig_radar.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself',
                    name=st_row['name'],
                    line_color="#6366f1"
                ))
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 100], gridcolor="#1e293b"),
                        bgcolor="rgba(0,0,0,0)"
                    ),
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#cbd5e1"),
                    height=320,
                    margin=dict(l=40, r=40, t=30, b=30)
                )
                st.plotly_chart(fig_radar)


# =========================================================
# PAGE 5: 🗄️ SQL INSIGHTS & EXPLORER
# =========================================================

elif page == "🗄️ SQL Insights":

    st.markdown(
        """
        <div class="hero-header">
            <div>
                <div class="page-title">🗄️ SQL Insights & Query Engine</div>
                <div class="page-subtitle">Pre-packaged database analytics and interactive SQL query runner</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    t1, t2 = st.tabs(["📈 Pre-packaged SQL Analytics", "⚡ Custom SQL Explorer"])

    with t1:
        col_sql1, col_sql2 = st.columns(2)

        with col_sql1:
            st.markdown('<div class="section-title">🏆 Top 10 High Achievers</div>', unsafe_allow_html=True)
            top_10 = df_filtered.sort_values("final_score", ascending=False).head(10)[
                ["student_id", "name", "city", "attendance", "final_score"]
            ]
            st.dataframe(top_10, hide_index=True)

        with col_sql2:
            st.markdown('<div class="section-title">⚠️ At-Risk Low Performers</div>', unsafe_allow_html=True)
            low_10 = df_filtered.sort_values("final_score", ascending=True).head(10)[
                ["student_id", "name", "city", "attendance", "study_hours", "final_score"]
            ]
            st.dataframe(low_10, hide_index=True)

        st.divider()

        col_sql3, col_sql4 = st.columns(2)

        with col_sql3:
            st.markdown('<div class="section-title">🏙️ City-wise Pass Percentage</div>', unsafe_allow_html=True)
            city_pass_df = (
                df_filtered.groupby("city")
                .agg(
                    Total=("student_id", "count"),
                    Passed=("result", lambda x: (x == "PASS").sum())
                )
                .reset_index()
            )
            city_pass_df["Pass_Percentage"] = (city_pass_df["Passed"] / city_pass_df["Total"] * 100).round(2)
            city_pass_df = city_pass_df.sort_values("Pass_Percentage", ascending=False)
            st.dataframe(city_pass_df, hide_index=True)

        with col_sql4:
            st.markdown('<div class="section-title">👫 Gender Performance Metrics</div>', unsafe_allow_html=True)
            gender_df = (
                df_filtered.groupby("gender")
                .agg(
                    Total_Students=("student_id", "count"),
                    Average_Score=("final_score", "mean"),
                    Avg_Study_Hours=("study_hours", "mean")
                )
                .reset_index()
            )
            gender_df["Average_Score"] = gender_df["Average_Score"].round(2)
            gender_df["Avg_Study_Hours"] = gender_df["Avg_Study_Hours"].round(2)
            st.dataframe(gender_df, hide_index=True)

    with t2:
        st.markdown('<div class="section-title">Execute Custom SELECT Queries</div>', unsafe_allow_html=True)
        default_query = "SELECT city, COUNT(*) AS student_count, ROUND(AVG(final_score), 2) AS avg_score FROM students s JOIN performance p ON s.student_id = p.student_id GROUP BY city ORDER BY avg_score DESC;"

        user_sql = st.text_area("SQL Query Box", value=default_query, height=120)
        run_sql = st.button("▶ Run SQL Query")

        if run_sql:
            if not user_sql.strip().lower().startswith("select"):
                st.error("Security Restriction: Only SELECT queries are permitted in this query explorer.")
            else:
                try:
                    if is_db_connected and HAS_DB_MODULE:
                        engine = create_engine_connection()
                        query_result = pd.read_sql(user_sql, engine)
                        st.success("Query executed successfully on MySQL live database!")
                        st.dataframe(query_result, hide_index=True)
                    else:
                        st.info("MySQL is offline. Executing simulated SQL query on in-memory dataset...")
                        # Run query against local dataframe table simulation
                        import sqlite3
                        import re
                        conn_mem = sqlite3.connect(":memory:")
                        df_raw.to_sql("performance_all", conn_mem, index=False)
                        # Replace JOIN syntax first, then standalone table names
                        # Use word boundaries to avoid double-replacing "performance_all"
                        sim_sql = user_sql.replace(
                            "students s JOIN performance p ON s.student_id = p.student_id",
                            "performance_all"
                        )
                        # Replace standalone "students" and "performance" (not already "performance_all")
                        sim_sql = re.sub(r'\bstudents\b', 'performance_all', sim_sql)
                        sim_sql = re.sub(r'\bperformance\b(?!_all)', 'performance_all', sim_sql)
                        # Fix any aliases like "s." or "p." -> remove them
                        sim_sql = re.sub(r'\bs\.', '', sim_sql)
                        sim_sql = re.sub(r'\bp\.', '', sim_sql)

                        res_df = pd.read_sql(sim_sql, conn_mem)
                        st.success("Query executed successfully on simulated dataset!")
                        st.dataframe(res_df, hide_index=True)
                except Exception as e:
                    st.error(f"SQL Execution Error: {e}")


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="custom-footer">
        StudentIQ Academic Performance Intelligence & Prediction Platform<br>
        Built with Python • Streamlit 1.61 • Plotly • MySQL • Scikit-Learn
    </div>
    """,
    unsafe_allow_html=True
)