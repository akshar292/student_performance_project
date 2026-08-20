import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor

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
print("       FEATURE IMPORTANCE")
print("======================================")


print(
    "\nTotal records:",
    len(df)
)


# ==========================================
# FEATURES
# ==========================================

features = [
    "attendance",
    "study_hours",
    "assignment_score",
    "midterm_score",
    "previous_score"
]


X = df[
    features
]


# ==========================================
# TARGET
# ==========================================

y = df[
    "final_score"
]


# ==========================================
# RANDOM FOREST
# ==========================================

model = RandomForestRegressor(

    n_estimators=100,

    random_state=42,

    n_jobs=-1
)


print(
    "\nTraining Random Forest..."
)


model.fit(
    X,
    y
)


# ==========================================
# FEATURE IMPORTANCE
# ==========================================

importance = pd.DataFrame(
    {
        "Feature": features,
        "Importance": model.feature_importances_
    }
)


importance = importance.sort_values(
    by="Importance",
    ascending=False
)


# ==========================================
# DISPLAY
# ==========================================

print(
    "\n===== FEATURE IMPORTANCE =====\n"
)


print(
    importance.to_string(
        index=False
    )
)


# ==========================================
# SAVE CSV
# ==========================================

importance.to_csv(
    "charts/feature_importance.csv",
    index=False
)


# ==========================================
# FEATURE IMPORTANCE CHART
# ==========================================

plt.figure(
    figsize=(9, 5)
)

plt.bar(
    importance["Feature"],
    importance["Importance"]
)

plt.xlabel(
    "Features"
)

plt.ylabel(
    "Importance"
)

plt.title(
    "Random Forest Feature Importance"
)

plt.xticks(
    rotation=30
)

plt.tight_layout()


plt.savefig(
    "charts/feature_importance.png"
)


plt.show()


# ==========================================
# BEST FEATURE
# ==========================================

best_feature = importance.iloc[0]["Feature"]

best_importance = importance.iloc[0]["Importance"]


print(
    "\nMost important feature:",
    best_feature
)


print(
    "Importance:",
    round(
        best_importance,
        4
    )
)


print(
    "\nFeature importance analysis completed successfully!"
)