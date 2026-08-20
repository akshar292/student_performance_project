import pandas as pd
import matplotlib.pyplot as plt
from db_connection import create_connection


def get_data():

    connection = create_connection()

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

    JOIN performance p
    ON s.student_id = p.student_id
    """

    df = pd.read_sql(query, connection)

    connection.close()

    return df


df = get_data()


# Attendance vs Final Score

plt.figure(figsize=(8, 5))

plt.scatter(
    df["attendance"],
    df["final_score"]
)

plt.xlabel("Attendance")
plt.ylabel("Final Score")
plt.title("Attendance vs Final Score")

plt.savefig("charts/attendance_vs_score.png")

plt.show()


# Study Hours vs Final Score

plt.figure(figsize=(8, 5))

plt.scatter(
    df["study_hours"],
    df["final_score"]
)

plt.xlabel("Study Hours")
plt.ylabel("Final Score")
plt.title("Study Hours vs Final Score")

plt.savefig("charts/study_hours_vs_score.png")

plt.show()