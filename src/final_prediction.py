import joblib
import pandas as pd


# ==========================================
# LOAD MODELS
# ==========================================

score_model = joblib.load(
    "models/best_student_model.pkl"
)

classification_model = joblib.load(
    "models/best_pass_fail_model.pkl"
)


# ==========================================
# HEADER
# ==========================================

print("\n======================================")
print("     STUDENT PERFORMANCE SYSTEM")
print("======================================")


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
# FINAL SCORE PREDICTION
# ==========================================

predicted_score = score_model.predict(
    student
)[0]


# Keep score between 0 and 100

predicted_score = max(
    0,
    min(
        100,
        predicted_score
    )
)


# ==========================================
# PASS / FAIL PREDICTION
# ==========================================

result = classification_model.predict(
    student
)[0]


# ==========================================
# PROBABILITY
# ==========================================

probabilities = classification_model.predict_proba(
    student
)[0]


fail_probability = probabilities[0] * 100

pass_probability = probabilities[1] * 100


# ==========================================
# DISPLAY RESULT
# ==========================================

print("\n======================================")

print(
    "Predicted Final Score:",
    round(
        predicted_score,
        2
    )
)


if result == 1:

    print(
        "Predicted Result: PASS"
    )

else:

    print(
        "Predicted Result: FAIL"
    )


print(
    "PASS Probability:",
    round(
        pass_probability,
        2
    ),
    "%"
)


print(
    "FAIL Probability:",
    round(
        fail_probability,
        2
    ),
    "%"
)


print("======================================")