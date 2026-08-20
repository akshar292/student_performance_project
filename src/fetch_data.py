from db_connection import create_connection


def fetch_students():

    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

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

    cursor.execute(query)

    records = cursor.fetchall()

    for student in records:
        print(student)

    cursor.close()
    connection.close()


if __name__ == "__main__":
    fetch_students()