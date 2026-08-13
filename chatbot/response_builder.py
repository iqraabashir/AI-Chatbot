import time
from chatbot.query_router import detect_query_type
import chatbot.query_router as qr

from chatbot.college_response import college_response
from chatbot.programme_search import search_programmes

from chatbot.pdf_search import search_pdf
from chatbot.programme_response import programme_response
from chatbot.knowledge_database import get_topic_fields, get_topic
from chatbot.semantic_search import find_best_topic
from chatbot.web_search import search_web_knowledge
from chatbot.university_response import university_response

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

def detect_query_type(user_question):
    question = user_question.lower()
    programme_keywords = [
        "programme", "program", "course", "degree", "admission", "eligibility",
        "fee", "duration", "semester", "curriculum", "syllabus", "selection process"
    ]
    college_keywords = [
        "college", "university", "campus", "hostel", "faculty", "department", "departments",
        "infrastructure", "ranking", "location"
    ]
    pdf_keywords = [
        "pdf", "document", "official document", "brochure", "prospectus",
        "handbook", "notice", "circular", "regulation"
    ]
    website_keywords = [
        "website", "web page", "official website", "link", "url", "online information"
    ]

    if any(keyword in question for keyword in programme_keywords):
        return "programme"
    if any(keyword in question for keyword in college_keywords):
        return "college"
    if any(keyword in question for keyword in pdf_keywords):
        return "pdf"
    if any(keyword in question for keyword in website_keywords):
        return "website"
    return "knowledge"


def build_response(user_question):
    print("\n===== RESPONSE BUILDER =====")
    print("Question:", user_question)
    start = time.time()
    query_type = qr.detect_query_type(user_question)

# universityinfo
    if query_type == "university":
        answer = university_response(user_question)
        print("University Time:", time.time() - start)

        if answer:
            return answer

        return "University information not found."
    
    #PROGRAMME 
    if query_type == "programme":
        answer = programme_response(user_question)
        print("Programme Time:", time.time() - start)
        if answer:
            return answer
        return "Programme information not found."

    #COLLEGE
    if query_type == "college":
        answer = college_response(user_question)
        print("College Time:", time.time() - start)
        if answer:
            return answer
        return "College information not found."

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