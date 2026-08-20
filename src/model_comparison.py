import pandas as pd
import joblib

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression

from sklearn.tree import DecisionTreeRegressor

from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from db_connection import create_connection


# ==========================================
# GET DATA
# ==========================================

def get_data():

    connection = create_connection()

    query = """
    SELECT
        attendance,
        study_hours,
        assignment_score,
        midterm_score,
        previous_score,
        final_score
    FROM performance
    """

    df = pd.read_sql(
        query,
        connection
    )

    connection.close()

    return df


# ==========================================
# LOAD DATA
# ==========================================

df = get_data()

print("\n===== DATASET =====")

print("Total records:", len(df))


# ==========================================
# FEATURES
# ==========================================

X = df[
    [
        "attendance",
        "study_hours",
        "assignment_score",
        "midterm_score",
        "previous_score"
    ]
]


# ==========================================
# TARGET
# ==========================================

y = df["final_score"]


# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


# ==========================================
# MODELS
# ==========================================

models = {

    "Linear Regression":
        LinearRegression(),

    "Decision Tree":
        DecisionTreeRegressor(
            max_depth=6,
            random_state=42
        ),

    "Random Forest":
        RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
}


# ==========================================
# TRAIN + EVALUATE
# ==========================================

results = []

trained_models = {}


for model_name, model in models.items():

    print(
        f"\nTraining {model_name}..."
    )

    # Train model

    model.fit(
        X_train,
        y_train
    )


    # Store trained model

    trained_models[model_name] = model


    # Predict

    predictions = model.predict(
        X_test
    )


    # Metrics

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    mse = mean_squared_error(
        y_test,
        predictions
    )

    rmse = mse ** 0.5

    r2 = r2_score(
        y_test,
        predictions
    )


    results.append(
        {
            "Model": model_name,
            "MAE": mae,
            "RMSE": rmse,
            "R2 Score": r2
        }
    )


# ==========================================
# RESULTS
# ==========================================

results_df = pd.DataFrame(
    results
)


results_df = results_df.sort_values(
    by="R2 Score",
    ascending=False
)


print("\n======================================")

print("        MODEL COMPARISON")

print("======================================\n")

print(
    results_df.to_string(
        index=False
    )
)


# ==========================================
# BEST MODEL
# ==========================================

best_model_name = results_df.iloc[0]["Model"]

best_model = trained_models[
    best_model_name
]


print(
    f"\nBest Model: {best_model_name}"
)


# ==========================================
# SAVE BEST MODEL
# ==========================================

joblib.dump(
    best_model,
    "models/best_student_model.pkl"
)


print(
    "\nBest model saved successfully!"
)

print(
    "File: models/best_student_model.pkl"
)