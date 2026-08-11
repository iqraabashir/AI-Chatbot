import sqlite3

conn = sqlite3.connect("chatbot/knowledge.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

for subject in ["mathematics", "urdu", "education"]:

    print("\n==============================")
    print("SUBJECT:", subject)
    print("==============================")

    cursor.execute("""
        SELECT
            programme,
            specialization,
            level,
            college,
            department,
            subject_overview
        FROM academic_programmes
        WHERE LOWER(programme) LIKE ?
           OR LOWER(specialization) LIKE ?
           OR LOWER(department) LIKE ?
    """, (
        f"%{subject}%",
        f"%{subject}%",
        f"%{subject}%"
    ))

    rows = cursor.fetchall()

    print("ROWS FOUND:", len(rows))

    for row in rows:
        print("Programme       :", row["programme"])
        print("Specialization  :", row["specialization"])
        print("Level           :", row["level"])
        print("College         :", row["college"])
        print("Department      :", row["department"])
        print("Subject Overview:", repr(row["subject_overview"]))
        print("------------------------------")

conn.close()


# import sqlite3

# conn = sqlite3.connect("chatbot/knowledge.db")
# cursor = conn.cursor()
# cursor.execute("""
# SELECT name
# FROM sqlite_master
# WHERE type='table'
# """)

# print(cursor.fetchall())

# print("\n===== knowledge_topics =====")
# cursor.execute("SELECT * FROM knowledge_topics")
# print(cursor.fetchall())

# print("\n===== knowledge_fields =====")
# cursor.execute("SELECT * FROM knowledge_fields")
# print(cursor.fetchall())

# print("\n===== knowledge_values =====")
# cursor.execute("SELECT * FROM knowledge_values")
# print(cursor.fetchall())

# conn.close()