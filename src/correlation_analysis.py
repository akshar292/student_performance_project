import pandas as pd
import matplotlib.pyplot as plt

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
print("       CORRELATION ANALYSIS")
print("======================================")


print(
    "\nTotal records:",
    len(df)
)


# ==========================================
# CORRELATION MATRIX
# ==========================================

correlation_matrix = df.corr()


print("\n===== CORRELATION MATRIX =====\n")

print(
    correlation_matrix.round(3)
)


# ==========================================
# FINAL SCORE CORRELATION
# ==========================================

final_correlation = (
    correlation_matrix["final_score"]
    .drop("final_score")
    .sort_values(
        ascending=False
    )
)


print(
    "\n======================================"
)

print(
    "  CORRELATION WITH FINAL SCORE"
)

print(
    "======================================\n"
)


print(
    final_correlation.round(3)
)


# ==========================================
# STRONGEST FEATURE
# ==========================================

strongest_feature = (
    final_correlation
    .abs()
    .idxmax()
)


strongest_value = (
    final_correlation[
        strongest_feature
    ]
)


print(
    "\nStrongest feature:",
    strongest_feature
)


print(
    "Correlation:",
    round(
        strongest_value,
        3
    )
)


# ==========================================
# SAVE CORRELATION DATA
# ==========================================

final_correlation.to_csv(
    "charts/final_score_correlation.csv"
)


# ==========================================
# CORRELATION BAR CHART
# ==========================================

plt.figure(
    figsize=(9, 5)
)

final_correlation.plot(
    kind="bar"
)

plt.xlabel(
    "Features"
)

plt.ylabel(
    "Correlation with Final Score"
)

plt.title(
    "Feature Correlation with Final Score"
)

plt.axhline(
    0
)

plt.tight_layout()


plt.savefig(
    "charts/final_score_correlation.png"
)


plt.show()


print(
    "\nCorrelation analysis completed successfully!"
)