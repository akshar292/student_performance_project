from db_connection import create_connection


def insert_student():

    connection = create_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO students
    (name, age, gender, city)
    VALUES (%s, %s, %s, %s)
    """

    values = (
        "Karan",
        21,
        "Male",
        "Ahmedabad"
    )

    cursor.execute(query, values)

    connection.commit()

    print("Student inserted successfully!")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    insert_student()