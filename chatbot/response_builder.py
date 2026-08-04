import time
from chatbot.query_router import detect_query_type
from chatbot.programme_search import search_programmes

from chatbot.pdf_search import search_pdf
from chatbot.programme_response import programme_response
from chatbot.knowledge_database import get_topic_fields, get_topic
from chatbot.semantic_search import find_best_topic
from chatbot.web_search import search_web_knowledge

def format_topic(topic_name):
    topic = get_topic(topic_name)
    if topic is None:
        return ""
    topic_id = topic[0]
    fields = get_topic_fields(topic_id)
    response = ""
    priority = [
        "Overview",
        "Programme Level",
        "Department",
        "Duration",
        "Eligibility",
        "Admission",
        "Admission Process",
        "Selection Process",
        "Documents",
        "Required Documents",
        "Examination Form",
        "Admit Card",
        "Date Sheet",
        "Result",
        "Re-evaluation",
        "Library Services",
        "Services",
        "Official Information",
        "Official Website",
        "Official Link"
    ]

    field_dict = {}
    for field in fields:
        field_dict[field[0]] = field[1]
    response += f"📘 {topic_name}\n\n"
    for item in priority:
        if item in field_dict:
            response += f"<b>{item}</b>\n"
            response += f"{field_dict[item]}\n\n"
    return response

def build_response(user_question):
    print("\n===== RESPONSE BUILDER =====")
    print("Question:", user_question)
    start = time.time()
    query_type = detect_query_type(user_question)
    print("Query Type:", query_type)

    #PROGRAMME 
    if query_type == "programme":
        answer = programme_response(user_question)
        print("Programme Time:", time.time() - start)
        if answer:
            return answer
        return "Programme information not found."

    #KNOWLEDGE
    if query_type == "knowledge":
        topic, score = find_best_topic(user_question)
        print("Topic:", topic)
        print("Score:", score)
        if topic and score >= 0.50:
            topic_name = topic[1]
            print("Knowledge Time:", time.time() - start)
            return format_topic(topic_name)
        return "Knowledge not found."

    #PDF 
    if query_type == "pdf":
        answer = programme_response(user_question)
        if answer:
            return answer
        
        pdf_result = search_pdf(user_question)
        print("PDF Time:", time.time() - start)
        if pdf_result:
            pdf_name, page, chunk = pdf_result
            return f"""
📄 <b>{pdf_name}</b>
<b>Page:</b> {page}
{chunk[:1500]}
"""
        return "Information not found in official documents."

    #WEBSITE
    if query_type == "website":
        web_result = search_web_knowledge(user_question)
        print("Website Time:", time.time() - start)
        if web_result:
            college, title, url, chunk, chunk_no = web_result
            return f"""
🌐 <b>{title}</b>
{chunk[:1500]}
<b>Source:</b>
{url}
"""
        return "Information not available."
    return "Sorry, I couldn't understand your question."