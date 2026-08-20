import pandas as pd
import matplotlib.pyplot as plt

from db_connection import create_engine_connection


# ==========================================
# GET DATA
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
print("        DATA VISUALIZATION")
print("======================================")


print(
    "\nDataset loaded successfully!"
)


print(
    "Total records:",
    len(df)
)


# ==========================================
# CHART 1
# ATTENDANCE VS FINAL SCORE
# ==========================================

plt.figure(
    figsize=(8, 5)
)

plt.scatter(
    df["attendance"],
    df["final_score"]
)

plt.xlabel(
    "Attendance (%)"
)

plt.ylabel(
    "Final Score"
)

plt.title(
    "Attendance vs Final Score"
)

plt.tight_layout()

plt.savefig(
    "charts/attendance_vs_score.png"
)

plt.show()


# ==========================================
# CHART 2
# STUDY HOURS VS FINAL SCORE
# ==========================================

plt.figure(
    figsize=(8, 5)
)

plt.scatter(
    df["study_hours"],
    df["final_score"]
)

plt.xlabel(
    "Study Hours"
)

plt.ylabel(
    "Final Score"
)

plt.title(
    "Study Hours vs Final Score"
)

plt.tight_layout()

plt.savefig(
    "charts/study_hours_vs_score.png"
)

plt.show()


# ==========================================
# CHART 3
# MIDTERM VS FINAL SCORE
# ==========================================

plt.figure(
    figsize=(8, 5)
)

plt.scatter(
    df["midterm_score"],
    df["final_score"]
)

plt.xlabel(
    "Midterm Score"
)

plt.ylabel(
    "Final Score"
)

plt.title(
    "Midterm Score vs Final Score"
)

plt.tight_layout()

plt.savefig(
    "charts/midterm_vs_final_score.png"
)

plt.show()


# ==========================================
# CHART 4
# FINAL SCORE DISTRIBUTION
# ==========================================

plt.figure(
    figsize=(8, 5)
)

plt.hist(
    df["final_score"],
    bins=20
)

plt.xlabel(
    "Final Score"
)

plt.ylabel(
    "Number of Students"
)

plt.title(
    "Final Score Distribution"
)

plt.tight_layout()

plt.savefig(
    "charts/final_score_distribution.png"
)

plt.show()


print(
    "\nAll charts generated successfully!"
)