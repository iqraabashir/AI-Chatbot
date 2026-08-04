import sqlite3
LAST_PROGRAMME = None

DATABASE_NAME = "chatbot/knowledge.db"


def search_programmes(user_question):

    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    question = user_question.lower()

    cursor.execute("""
        SELECT *
        FROM academic_programmes
    """)

    programmes = cursor.fetchall()

    conn.close()

    best_match = None
    best_score = 0

    for programme in programmes:

        score = 0

        name = programme["programme_name"].lower()

        college = (programme["college"] or "").lower()

        department = (programme["department"] or "").lower()

        words = name.split()

        for word in words:

            if len(word) > 2 and word in question:
                score += 3

        if name in question:
            score += 10

        if college and college in question:
            score += 2

        if department and department in question:
            score += 2

        if score > best_score:

            best_score = score
            best_match = programme

    global LAST_PROGRAMME

    if best_match:
       LAST_PROGRAMME = best_match

    return best_match

def get_last_programme():

    global LAST_PROGRAMME

    return LAST_PROGRAMME