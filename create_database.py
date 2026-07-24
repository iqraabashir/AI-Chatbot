from chatbot.database import create_tables, add_answer, add_question
create_tables()
answer_id = add_answer(
    intent="Admission",
    answer="Admissions are open. Please visit the official admission section on the Cluster University Srinagar website.",
    category="Admission",
    source="Cluster University Srinagar Website",
    last_updated="2026-07-17"
)

# Insert related questions
add_question(answer_id, "How can I apply for admission?", "admission apply")
add_question(answer_id, "Admission process", "admission process")
add_question(answer_id, "How do I get admission?", "admission")

print("Sample FAQ inserted successfully!")


