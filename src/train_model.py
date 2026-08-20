import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from db_connection import create_engine_connection


# ==========================================
# GET DATA FROM MYSQL
# ==========================================

def get_data():

    # Create SQLAlchemy engine
    engine = create_engine_connection()

    # SQL query
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

    # Read data using Pandas + SQLAlchemy
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
print("        STUDENT PERFORMANCE DATA")
print("======================================")

print(
    "\nTotal records:",
    len(df)
)


print("\nDataset:")

print(
    df.head()
)


# ==========================================
# CHECK EMPTY DATASET
# ==========================================

if df.empty:

    raise ValueError(
        "Dataset is empty. Please check your MySQL database."
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

y = df[
    "final_score"
]


# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42
)


print("\n======================================")
print("          DATA SPLIT")
print("======================================")

print(
    "Training records:",
    len(X_train)
)

print(
    "Testing records:",
    len(X_test)
)


# ==========================================
# CREATE MODEL
# ==========================================

model = LinearRegression()


# ==========================================
# TRAIN MODEL
# ==========================================

print("\nTraining Linear Regression...")

model.fit(
    X_train,
    y_train
)


# ==========================================
# PREDICTION
# ==========================================

predictions = model.predict(
    X_test
)


# ==========================================
# MODEL EVALUATION
# ==========================================

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


# ==========================================
# DISPLAY RESULTS
# ==========================================

print("\n======================================")
print("        MODEL PERFORMANCE")
print("======================================")

print(
    "MAE:",
    mae
)

print(
    "MSE:",
    mse
)

print(
    "RMSE:",
    rmse
)

print(
    "R2 Score:",
    r2
)


# ==========================================
# SAVE MODEL
# ==========================================

joblib.dump(
    model,
    "models/student_score_model.pkl"
)


print("\n======================================")

print(
    "Model saved successfully!"
)

print(
    "File: models/student_score_model.pkl"
)

print("======================================")