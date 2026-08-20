import pandas as pd
import joblib

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

from db_connection import create_engine_connection


# ==========================================
# GET DATA FROM MYSQL
# ==========================================

def get_data():

    engine = create_engine_connection()

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
        engine
    )

    return df


# ==========================================
# LOAD DATA
# ==========================================

df = get_data()


print("\n======================================")
print("       STUDENT CLASSIFICATION")
print("======================================")


print(
    "\nTotal records:",
    len(df)
)


# ==========================================
# CHECK DATA
# ==========================================

if df.empty:

    raise ValueError(
        "Dataset is empty. Please check MySQL database."
    )


# ==========================================
# CREATE PASS / FAIL
# ==========================================

df["result"] = df["final_score"].apply(
    lambda score: 1
    if score >= 40
    else 0
)


print(
    "\n===== RESULT DISTRIBUTION ====="
)

print(
    df["result"].value_counts()
)


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

y = df["result"]


# ==========================================
# CHECK CLASSES
# ==========================================

if y.nunique() < 2:

    raise ValueError(
        "Classification requires both PASS and FAIL classes."
    )


# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)


print(
    "\nTraining records:",
    len(X_train)
)

print(
    "Testing records:",
    len(X_test)
)


# ==========================================
# MODELS
# ==========================================

models = {

    "Logistic Regression":
        LogisticRegression(
            max_iter=1000
        ),

    "Random Forest":
        RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
}


# ==========================================
# TRAIN MODELS
# ==========================================

results = []

trained_models = {}


for model_name, model in models.items():

    print(
        f"\nTraining {model_name}..."
    )


    # Train

    model.fit(
        X_train,
        y_train
    )


    # Save trained model in memory

    trained_models[
        model_name
    ] = model


    # Prediction

    predictions = model.predict(
        X_test
    )


    # ======================================
    # METRICS
    # ======================================

    accuracy = accuracy_score(
        y_test,
        predictions
    )


    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )


    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )


    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )


    results.append(
        {
            "Model": model_name,
            "Accuracy": accuracy,
            "Precision": precision,
            "Recall": recall,
            "F1 Score": f1
        }
    )


    # ======================================
    # MODEL RESULTS
    # ======================================

    print(
        f"\n===== {model_name} ====="
    )


    print(
        "Accuracy:",
        accuracy
    )


    print(
        "Precision:",
        precision
    )


    print(
        "Recall:",
        recall
    )


    print(
        "F1 Score:",
        f1
    )


    # ======================================
    # CONFUSION MATRIX
    # ======================================

    print(
        "\nConfusion Matrix:"
    )


    print(
        confusion_matrix(
            y_test,
            predictions
        )
    )


    # ======================================
    # CLASSIFICATION REPORT
    # ======================================

    print(
        "\nClassification Report:"
    )


    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )


# ==========================================
# COMPARISON
# ==========================================

results_df = pd.DataFrame(
    results
)


results_df = results_df.sort_values(
    by="F1 Score",
    ascending=False
)


print(
    "\n======================================"
)

print(
    "     CLASSIFICATION COMPARISON"
)

print(
    "======================================\n"
)


print(
    results_df.to_string(
        index=False
    )
)


# ==========================================
# BEST MODEL
# ==========================================

best_model_name = (
    results_df.iloc[0]["Model"]
)


best_model = trained_models[
    best_model_name
]


print(
    "\nBest Classification Model:",
    best_model_name
)


# ==========================================
# SAVE BEST MODEL
# ==========================================

joblib.dump(
    best_model,
    "models/best_pass_fail_model.pkl"
)


print(
    "\nBest classification model saved!"
)


print(
    "File: models/best_pass_fail_model.pkl"
)