import pandas as pd

from db_connection import create_engine_connection


# ==========================================
# DATABASE ENGINE
# ==========================================

engine = create_engine_connection()


print("\n======================================")
print("           SQL ANALYSIS")
print("======================================")


# ==========================================
# 1. TOTAL STUDENTS
# ==========================================

query = """
SELECT
    COUNT(*) AS total_students
FROM students
"""


result = pd.read_sql(
    query,
    engine
)


print(
    "\n===== TOTAL STUDENTS ====="
)

print(
    result.to_string(
        index=False
    )
)


# ==========================================
# 2. AVERAGE FINAL SCORE
# ==========================================

query = """
SELECT
    ROUND(
        AVG(final_score),
        2
    ) AS average_final_score

FROM performance
"""


result = pd.read_sql(
    query,
    engine
)


print(
    "\n===== AVERAGE FINAL SCORE ====="
)

print(
    result.to_string(
        index=False
    )
)


# ==========================================
# 3. CITY-WISE PERFORMANCE
# ==========================================

query = """
SELECT

    s.city,

    COUNT(*) AS total_students,

    ROUND(
        AVG(p.final_score),
        2
    ) AS average_score

FROM students s

INNER JOIN performance p

ON s.student_id = p.student_id

GROUP BY
    s.city

ORDER BY
    average_score DESC
"""


result = pd.read_sql(
    query,
    engine
)


print(
    "\n===== CITY-WISE PERFORMANCE ====="
)

print(
    result.to_string(
        index=False
    )
)


# ==========================================
# 4. TOP 10 STUDENTS
# ==========================================

query = """
SELECT

    s.student_id,

    s.name,

    s.city,

    p.attendance,

    p.final_score

FROM students s

INNER JOIN performance p

ON s.student_id = p.student_id

ORDER BY
    p.final_score DESC

LIMIT 10
"""


result = pd.read_sql(
    query,
    engine
)


print(
    "\n===== TOP 10 STUDENTS ====="
)

print(
    result.to_string(
        index=False
    )
)


# ==========================================
# 5. LOW PERFORMERS
# ==========================================

query = """
SELECT

    s.student_id,

    s.name,

    s.city,

    p.attendance,

    p.study_hours,

    p.final_score

FROM students s

INNER JOIN performance p

ON s.student_id = p.student_id

WHERE
    p.final_score < 40

ORDER BY
    p.final_score ASC
"""


result = pd.read_sql(
    query,
    engine
)


print(
    "\n===== LOW PERFORMERS ====="
)

print(
    result.to_string(
        index=False
    )
)


# ==========================================
# 6. PASS / FAIL DISTRIBUTION
# ==========================================

query = """
SELECT

    CASE
        WHEN final_score >= 40
        THEN 'PASS'

        ELSE 'FAIL'

    END AS result,

    COUNT(*) AS total_students

FROM performance

GROUP BY

    CASE
        WHEN final_score >= 40
        THEN 'PASS'

        ELSE 'FAIL'

    END

ORDER BY
    result
"""


result = pd.read_sql(
    query,
    engine
)


print(
    "\n===== PASS / FAIL DISTRIBUTION ====="
)

print(
    result.to_string(
        index=False
    )
)


# ==========================================
# 7. CITY-WISE PASS RATE
# ==========================================

query = """
SELECT

    s.city,

    COUNT(*) AS total_students,

    SUM(
        CASE
            WHEN p.final_score >= 40
            THEN 1
            ELSE 0
        END
    ) AS passed_students,

    ROUND(

        SUM(
            CASE
                WHEN p.final_score >= 40
                THEN 1
                ELSE 0
            END
        )
        * 100.0
        / COUNT(*),

        2

    ) AS pass_percentage

FROM students s

INNER JOIN performance p

ON s.student_id = p.student_id

GROUP BY
    s.city

ORDER BY
    pass_percentage DESC
"""


result = pd.read_sql(
    query,
    engine
)


print(
    "\n===== CITY-WISE PASS RATE ====="
)

print(
    result.to_string(
        index=False
    )
)


print(
    "\n======================================"
)

print(
    "       SQL ANALYSIS COMPLETED"
)

print(
    "======================================"
)