import sqlite3

DATABASE_NAME = "chatbot/faq.db"


def search_web_knowledge(user_question):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    question = user_question.lower().strip()

    # ---------------------------------------------------------
    # OFFICIAL UNIVERSITY WEBSITE
    # ---------------------------------------------------------

    if (
        "official website" in question
        or question in [
            "website",
            "university website",
            "official university website"
        ]
    ):
        cursor.execute("""
            SELECT
                college,
                page_title,
                url,
                chunk_text,
                chunk_no
            FROM web_chunks
            WHERE LOWER(url) = ?
            LIMIT 1
        """, (
            "https://www.cusrinagar.edu.in/",
        ))

        row = cursor.fetchone()

        if row:
            conn.close()
            return row

    # ---------------------------------------------------------
    # RESULT QUERIES
    # ---------------------------------------------------------

    result_query = (
        "result" in question
        or "results" in question
    )

    if result_query:

        cursor.execute("""
            SELECT
                college,
                page_title,
                url,
                chunk_text,
                chunk_no
            FROM web_chunks
            WHERE LOWER(page_title) LIKE '%result notification%'
            ORDER BY
                CASE
                    WHEN LOWER(url) LIKE '%program=PG%' THEN 0
                    WHEN LOWER(url) LIKE '%program=UG%' THEN 1
                    WHEN LOWER(url) LIKE '%program=BED%' THEN 2
                    WHEN LOWER(url) LIKE '%program=IH%' THEN 3
                    ELSE 4
                END
            LIMIT 1
        """)

        row = cursor.fetchone()

        if row:
            conn.close()
            return row

    # ---------------------------------------------------------
    # NOTIFICATION / EXAM NOTIFICATION QUERIES
    # ---------------------------------------------------------

    notification_query = (
        "notification" in question
        or "notifications" in question
        or "notice" in question
        or "notices" in question
        or "circular" in question
        or "circulars" in question
        or "latest" in question
    )

    if notification_query:

        cursor.execute("""
            SELECT
                college,
                page_title,
                url,
                chunk_text,
                chunk_no
            FROM web_chunks
            WHERE LOWER(page_title) LIKE '%notification%'
            AND LOWER(url) LIKE '%/Notification/Notification%'
            LIMIT 1
        """)

        row = cursor.fetchone()

        if row:
            conn.close()
            return row

    # ---------------------------------------------------------
    # GENERAL WEBSITE SEARCH
    # ---------------------------------------------------------

    words = question.split()

    stop_words = {
        "show",
        "me",
        "the",
        "what",
        "are",
        "is",
        "of",
        "for",
        "please",
        "give",
        "tell",
        "about",
        "find",
        "latest",
        "current",
        "official"
    }

    words = [
        word
        for word in words
        if word not in stop_words
    ]

    if words:

        conditions = " AND ".join(
            ["LOWER(chunk_text) LIKE ?" for _ in words]
        )

        parameters = [
            f"%{word}%"
            for word in words
        ]

        cursor.execute(
            f"""
            SELECT
                college,
                page_title,
                url,
                chunk_text,
                chunk_no
            FROM web_chunks
            WHERE {conditions}
            LIMIT 1
            """,
            parameters
        )

        row = cursor.fetchone()

        if row:
            conn.close()
            return row

    conn.close()
    return None