import sqlite3

DATABASE_NAME = "chatbot/knowledge.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Stores every main topic
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_topics(
            topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT
        )
    """)

    # Stores fields related to a topic
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_fields(
            field_id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id INTEGER NOT NULL,
            field_name TEXT NOT NULL,
            FOREIGN KEY(topic_id) REFERENCES knowledge_topics(topic_id)
        )
    """)

    # Stores the actual values
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_values(
            value_id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_id INTEGER NOT NULL,
            field_value TEXT NOT NULL,
            source TEXT,
            url TEXT,
            last_updated TEXT,
            FOREIGN KEY(field_id) REFERENCES knowledge_fields(field_id)
        )
    """)

    # Stores latest university notifications
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications(
            notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT,
            summary TEXT,
            publish_date TEXT,
            url TEXT
        )
    """)

    # Stores chat history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history(
            chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_question TEXT,
            bot_response TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def add_topic(topic_name, category, description):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO knowledge_topics (topic_name, category, description)
        VALUES (?, ?, ?)
    """, (topic_name, category, description))

    conn.commit()
    topic_id = cursor.lastrowid
    conn.close()

    return topic_id


def add_field(topic_id, field_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO knowledge_fields (topic_id, field_name)
        VALUES (?, ?)
    """, (topic_id, field_name))

    conn.commit()
    field_id = cursor.lastrowid
    conn.close()

    return field_id


def add_value(field_id, field_value, source, url, last_updated):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO knowledge_values
        (field_id, field_value, source, url, last_updated)
        VALUES (?, ?, ?, ?, ?)
    """, (field_id, field_value, source, url, last_updated))

    conn.commit()
    conn.close()

def get_topic(topic_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT topic_id, topic_name, category, description
        FROM knowledge_topics
        WHERE LOWER(topic_name)=LOWER(?)
    """, (topic_name,))

    result = cursor.fetchone()
    conn.close()

    return result


def get_topic_fields(topic_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            knowledge_fields.field_name,
            knowledge_values.field_value,
            knowledge_values.source,
            knowledge_values.url,
            knowledge_values.last_updated
        FROM knowledge_fields
        JOIN knowledge_values
        ON knowledge_fields.field_id = knowledge_values.field_id
        WHERE knowledge_fields.topic_id = ?
    """, (topic_id,))

    result = cursor.fetchall()
    conn.close()

    return result

def get_all_topics():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT topic_id, topic_name
        FROM knowledge_topics
    """)

    topics = cursor.fetchall()

    conn.close()

    return topics

def get_search_records():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            knowledge_topics.topic_id,
            knowledge_topics.topic_name,
            knowledge_fields.field_name,
            knowledge_values.field_value
        FROM knowledge_topics
        JOIN knowledge_fields
            ON knowledge_topics.topic_id = knowledge_fields.topic_id
        JOIN knowledge_values
            ON knowledge_fields.field_id = knowledge_values.field_id
    """)

    records = cursor.fetchall()
    conn.close()
    return records