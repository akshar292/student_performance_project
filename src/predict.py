import joblib
import pandas as pd


# ==========================================
# LOAD BEST MODEL
# ==========================================

model = joblib.load(
    "models/best_student_model.pkl"
)


print("\n====================================")
print("   STUDENT PERFORMANCE PREDICTOR")
print("====================================")


# ==========================================
# USER INPUT
# ==========================================

attendance = float(
    input("\nEnter Attendance (%): ")
)

study_hours = float(
    input("Enter Study Hours: ")
)

assignment_score = float(
    input("Enter Assignment Score: ")
)

midterm_score = float(
    input("Enter Midterm Score: ")
)

previous_score = float(
    input("Enter Previous Score: ")
)


# ==========================================
# CREATE DATAFRAME
# ==========================================

student = pd.DataFrame(
    {
        "attendance": [attendance],
        "study_hours": [study_hours],
        "assignment_score": [assignment_score],
        "midterm_score": [midterm_score],
        "previous_score": [previous_score]
    }
)


# ==========================================
# PREDICTION
# ==========================================

predicted_score = model.predict(
    student
)[0]


predicted_score = max(
    0,
    min(
        100,
        predicted_score
    )
)


# ==========================================
# RESULT
# ==========================================

print("\n====================================")

print(
    "Predicted Final Score:",
    round(predicted_score, 2)
)


if predicted_score >= 40:

    print("Predicted Result: PASS")

else:

    print("Predicted Result: FAIL")


print("====================================")