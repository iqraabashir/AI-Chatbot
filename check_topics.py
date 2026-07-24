import sqlite3

conn = sqlite3.connect("chatbot/knowledge.db")
cursor = conn.cursor()

print("\n===== knowledge_topics =====")
cursor.execute("SELECT * FROM knowledge_topics")
print(cursor.fetchall())

print("\n===== knowledge_fields =====")
cursor.execute("SELECT * FROM knowledge_fields")
print(cursor.fetchall())

print("\n===== knowledge_values =====")
cursor.execute("SELECT * FROM knowledge_values")
print(cursor.fetchall())

conn.close()