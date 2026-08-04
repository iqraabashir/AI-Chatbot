import sqlite3

DATABASE_NAME = "chatbot/faq.db"

def search_pdf(user_question):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    words = user_question.lower().split()

    best_result = None

    for word in words:

        cursor.execute("""

        SELECT
            pdf_name,
            page,
            chunk

        FROM pdf_knowledge

        WHERE
            LOWER(chunk) LIKE ?

        LIMIT 1

        """, (f"%{word}%",))

        row = cursor.fetchone()

        if row:
            best_result = row
            break

    conn.close()
    return best_result