import random
import mysql.connector


# ==========================================
# DATABASE CONNECTION
# ==========================================

def create_connection():

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="student_ml_project",
        port=3307
    )

    return connection


# ==========================================
# SAMPLE DATA
# ==========================================

first_names = [
    "Rahul",
    "Rohan",
    "Raj",
    "Vivek",
    "Arjun",
    "Yash",
    "Harsh",
    "Dev",
    "Jay",
    "Krish",
    "Neha",
    "Pooja",
    "Riya",
    "Sneha",
    "Anjali",
    "Kavya",
    "Nisha",
    "Simran"
]


cities = [
    "Ahmedabad",
    "Surat",
    "Vadodara",
    "Rajkot",
    "Gandhinagar",
    "Mumbai",
    "Delhi",
    "Pune"
]


genders = [
    "Male",
    "Female"
]


# ==========================================
# GENERATE PERFORMANCE
# ==========================================

def generate_performance(result_type):

    if result_type == "FAIL":

        attendance = round(
            random.uniform(40, 69),
            2
        )

        study_hours = round(
            random.uniform(0.5, 2.5),
            2
        )

        assignment_score = random.randint(
            20,
            55
        )

        midterm_score = random.randint(
            20,
            55
        )

        previous_score = random.randint(
            20,
            55
        )


    else:

        attendance = round(
            random.uniform(70, 100),
            2
        )

        study_hours = round(
            random.uniform(3, 8),
            2
        )

        assignment_score = random.randint(
            55,
            100
        )

        midterm_score = random.randint(
            50,
            100
        )

        previous_score = random.randint(
            50,
            100
        )


    # ======================================
    # FINAL SCORE
    # ======================================

    final_score = (

        attendance * 0.20

        + study_hours * 2.0

        + assignment_score * 0.25

        + midterm_score * 0.30

        + previous_score * 0.15

    )


    # Small random noise

    final_score += random.uniform(
        -5,
        5
    )


    # Keep score 0-100

    final_score = max(
        0,
        min(
            100,
            final_score
        )
    )


    final_score = round(
        final_score,
        2
    )


    return (
        attendance,
        study_hours,
        assignment_score,
        midterm_score,
        previous_score,
        final_score
    )


# ==========================================
# GENERATE STUDENTS
# ==========================================

def generate_students():

    connection = create_connection()

    cursor = connection.cursor()


    student_query = """
    INSERT INTO students
    (
        name,
        age,
        gender,
        city
    )
    VALUES
    (
        %s,
        %s,
        %s,
        %s
    )
    """


    performance_query = """
    INSERT INTO performance
    (
        student_id,
        attendance,
        study_hours,
        assignment_score,
        midterm_score,
        previous_score,
        final_score
    )
    VALUES
    (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
    )
    """


    # ======================================
    # CREATE RESULT LIST
    # ======================================

    result_types = (
        ["PASS"] * 800
        +
        ["FAIL"] * 200
    )


    # Shuffle

    random.shuffle(
        result_types
    )


    # ======================================
    # INSERT 1000 STUDENTS
    # ======================================

    for i, result_type in enumerate(
        result_types,
        start=1
    ):

        # Student information

        name = random.choice(
            first_names
        )

        age = random.randint(
            18,
            24
        )

        gender = random.choice(
            genders
        )

        city = random.choice(
            cities
        )


        # Performance

        performance = generate_performance(
            result_type
        )


        # Insert student

        cursor.execute(
            student_query,
            (
                name,
                age,
                gender,
                city
            )
        )


        student_id = cursor.lastrowid


        # Insert performance

        cursor.execute(
            performance_query,
            (
                student_id,
                performance[0],
                performance[1],
                performance[2],
                performance[3],
                performance[4],
                performance[5]
            )
        )


        if i % 100 == 0:

            print(
                f"{i} students inserted..."
            )


    connection.commit()


    cursor.close()

    connection.close()


    print(
        "\n1000 students inserted successfully!"
    )


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    generate_students()