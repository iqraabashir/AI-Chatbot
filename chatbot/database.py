import sqlite3
from difflib import SequenceMatcher


DATABASE_NAME = "chatbot/faq.db"


def get_connection():
  
    connection = sqlite3.connect(DATABASE_NAME)

    return connection
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
         CREATE TABLE IF NOT EXISTS answers (
            answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            answer TEXT NOT NULL,
            intent TEXT NOT NULL,
            category TEXT,
            source TEXT,
            last_updated TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions(
                   question_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   answer_id INTEGER,
                   question TEXT NOT NULL,
                   keywords TEXT,
                   FOREIGN KEY (answer_id) REFERENCES answers(answer_id)
            )
    ''')
    cursor.execute('''
           CREATE TABLE IF NOT EXISTS chat_history(
                   chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_question TEXT,
                   bot_answer TEXT,
                   timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                   language TEXT
            )
    ''')
    conn.commit()
    conn.close()

def add_answer(answer, intent, category, source, last_updated):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO answers (answer, intent, category, source, last_updated)
        VALUES (?, ?, ?, ?, ?)
    ''', (answer, intent, category, source, last_updated))

    conn.commit()
    answer_id = cursor.lastrowid
    conn.close()
    return answer_id

def add_question(answer_id, question, keywords):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO questions (answer_id, question, keywords)
        VALUES (?, ?, ?)
    ''', (answer_id, question, keywords))

    conn.commit()
    conn.close() 

def search_question(user_question):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT questions.question, answers.answer
        FROM questions
        JOIN answers
        ON questions.answer_id = answers.answer_id
    """)

    rows = cursor.fetchall()
    conn.close()

    best_match = None
    highest_score = 0

    user_question = user_question.lower()

    for question, answer in rows:

        score = SequenceMatcher(
            None,
            user_question,
            question.lower()
        ).ratio()

        if score > highest_score:
            highest_score = score
            best_match = answer

    # Minimum similarity required
    if highest_score >= 0.60:
        return best_match

    return None