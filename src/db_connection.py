import mysql.connector

from sqlalchemy import create_engine


# ==========================================
# MYSQL CONNECTOR
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
# SQLALCHEMY ENGINE
# ==========================================

def create_engine_connection():

    engine = create_engine(
        "mysql+mysqlconnector://root:@localhost:3307/student_ml_project"
    )

    return engine