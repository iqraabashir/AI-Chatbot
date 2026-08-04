import sqlite3

DATABASE_NAME = "chatbot/faq.db"

def search_web_knowledge(user_question):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    words = user_question.lower().split()
    best_result = None
    for word in words:
        cursor.execute("""
        SELECT
            college,
            page_title,
            url,
            chunk_text,
            chunk_no

        FROM web_chunks
        WHERE
            LOWER(chunk_text) LIKE ?
        LIMIT 1
        """, (f"%{word}%",))
        row = cursor.fetchone()
        if row:
            best_result = row
            break
    conn.close()
    return best_result