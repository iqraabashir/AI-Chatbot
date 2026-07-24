from chatbot.knowledge_database import get_topic_fields, get_topic
from chatbot.semantic_search import find_best_topic


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

    topic, score = find_best_topic(user_question)

    if topic is None or score < 0.50:
        return "Sorry, I couldn't find relevant information."

    topic_name = topic[1]

    final_response = ""

    # Main Topic
    final_response += format_topic(topic_name)

    question = user_question.lower()

    # Related Information

    if "admission" in question:
        if topic_name != "General Admission":
            final_response += "\n"
            final_response += format_topic("General Admission")

    if "exam" in question:
        if topic_name != "Examinations":
            final_response += "\n"
            final_response += format_topic("Examinations")

    if "scholarship" in question:
        if topic_name != "Scholarships":
            final_response += "\n"
            final_response += format_topic("Scholarships")

    if "library" in question:
        if topic_name != "Library":
            final_response += "\n"
            final_response += format_topic("Library")

    if "college" in question:
        if topic_name != "Constituent Colleges":
            final_response += "\n"
            final_response += format_topic("Constituent Colleges")

    return final_response