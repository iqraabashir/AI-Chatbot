import time
# from chatbot.query_router import detect_query_type
import chatbot.query_router as qr

from chatbot.college_response import college_response
from chatbot.general_admission import get_general_admission_response
from chatbot.programme_search import search_programmes

from chatbot.pdf_search import search_pdf
from chatbot.programme_response import programme_response
from chatbot.knowledge_database import get_topic_fields, get_topic
from chatbot.semantic_search import find_best_topic
from chatbot.web_search import search_web_knowledge
from chatbot.university_response import university_response
from datetime import datetime

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
    query_type = qr.detect_query_type(user_question)
    
    general_admission_response = get_general_admission_response(
    user_question
    )
    if general_admission_response:
       print("General Admission Time:", time.time() - start)
       return general_admission_response
        # SYLLABUS
    if "syllabus" in user_question.lower():
        return (
            "📚 <b>University Syllabus</b><br><br>"
            "You can view the official Cluster University Srinagar "
            "syllabus here:<br><br>"
            '<a href="https://www.cusrinagar.edu.in/Syllabus/Index/True?pp=UG" '
            'target="_blank">📖 View Official Syllabus</a>'
        )

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
        question_lower = user_question.lower().strip()
        if (
            "prospectus" in question_lower
            and not any(
                word in question_lower
                for word in ["page", "pages"]
            )
        ):
            return (
               "📄 <b>Cluster University of Srinagar – E-Prospectus</b>\n\n"
               "The official university prospectus is available here.\n\n"
               '🔗 <a href="/prospectus" target="_blank">View Prospectus</a>'
            )
        pdf_result = search_pdf(user_question)
        print("PDF Time:", time.time() - start)
        if pdf_result:
           pdf_name, page, chunk = pdf_result
           if pdf_name.lower() == "prospectus.pdf":
              question_lower = user_question.lower()
              import re
              page_match = re.search(
                r"\bpage\s*(?:no\.?|number)?\s*(\d+)\b",
                question_lower
              )
              if page_match:
                 requested_page = page_match.group(1)
                 return (
                    f"📄 <b>Cluster University of Srinagar – "
                    f"E-Prospectus</b>\n\n"
                    f"📑 <b>Page {requested_page}</b>\n\n"
                    f"{chunk[:2000]}\n\n"
                    f'🔗 <a href="/prospectus" target="_blank">'
                    f"View Full Prospectus</a>"
                )

            # Normal prospectus question
              return (
                "📄 <b>Cluster University of Srinagar – "
                "E-Prospectus</b>\n\n"
                "The official university prospectus is available here.\n\n"
                '🔗 <a href="/prospectus" target="_blank">'
                "View Prospectus</a>"
              )

        # Other official PDF documents
           return (
            f"📄 <b>{pdf_name}</b>\n\n"
            f"📑 <b>Page:</b> {page}\n\n"
            f"{chunk[:2000]}"
        )

        # WEBSITE
    if query_type == "website":
        web_result = search_web_knowledge(user_question)
        print("Website Time:", time.time() - start)
        if not web_result:
            return "Information not available."

        # STRUCTURED WEBSITE DATA
        if isinstance(web_result, dict):
            result_type = web_result.get("type")
            items = web_result.get("items", [])

            # LATEST NOTIFICATIONS
            if result_type == "notifications":
                response = (
                    "🔔 <b>Latest Notifications – "
                    "Cluster University Srinagar</b>\n\n"
                )
                for item in items:
                    item_type, title, item_date, url = item
                    response += f"📌 <b>{title}</b>\n"
                    if item_date:
                        try:
                            display_date = datetime.strptime(
                              item_date,
                              "%Y-%m-%d"
                            ).strftime("%d-%B-%Y")
                        except ValueError:
                            display_date = item_date
                        response += f"📅 {display_date}\n"

                        # response += f"📅 {item_date}\n"
                    if url:
                        response += (
                            f'🔗 <a href="{url}" target="_blank">'
                            "View Notification</a>\n"
                        )
                    response += "\n"
                response += (
                    "🌐 <b>Source:</b> "
                    '<a href="https://www.cusrinagar.edu.in/Notification/Notification" '
                    'target="_blank">Official CUS Notification Section</a>'
                )
                return response

            # EXAMINATION NOTIFICATIONS
            if result_type == "exam_notifications":
                response = (
                    "📝 <b>Latest Examination Notifications – "
                    "Cluster University Srinagar</b>\n\n"
                )
                for item in items:
                    item_type, title, item_date, url = item
                    response += f"📌 <b>{title}</b>\n"
                    if item_date:   
                        try:
                            display_date = datetime.strptime(
                               item_date,
                               "%Y-%m-%d"
                            ).strftime("%d-%B-%Y")
                        except ValueError:
                            display_date = item_date
                        response += f"📅 {display_date}\n"
                        #response += f"📅 {item_date}\n"
                    if url:
                        response += (
                            f'🔗 <a href="{url}" target="_blank">'
                            "View Notification</a>\n"
                        )
                    response += "\n"
                response += (
                    "🌐 <b>Source:</b> "
                    '<a href="https://www.cusrinagar.edu.in/Notification/Notification" '
                    'target="_blank">Official CUS Notification Section</a>'
                )
                return response

            if result_type == "admission_notifications":
                response = (
                    "🎓 <b>Latest Admission Notifications – "
                    "Cluster University Srinagar</b>\n\n"
                )
                for item in items:
                    item_type, title, item_date, url = item
                    response += f"📌 <b>{title}</b>\n"
                    if item_date:
                      try:
                         display_date = datetime.strptime(
                         item_date,
                         "%Y-%m-%d"
                         ).strftime("%d-%B-%Y")
                      except ValueError:
                         display_date = item_date
                      response += f"📅 {display_date}\n"
                    if url:
                        response += (
                          f'🔗 <a href="{url}" target="_blank">'
                          "View Notification</a>\n"
                        )
                    response += "\n"
                response += (
                  "🌐 <b>Source:</b> "
                  '<a href="https://www.cusrinagar.edu.in/Notification/Notification" '
                  'target="_blank">Official CUS Notification Section</a>'
                )
                return response

            if result_type == "job_notifications":
                response = (
                "💼 <b>Latest Job Notifications – "
                "Cluster University Srinagar</b>\n\n"
                )
                for item in items:
                    item_type, title, item_date, url = item
                    response += f"📌 <b>{title}</b>\n"
                    if item_date:
                        try:
                            display_date = datetime.strptime(
                                item_date,
                                "%Y-%m-%d"
                                ).strftime("%d-%B-%Y")
                        except ValueError:
                            display_date = item_date
                        response += f"📅 {display_date}\n"
                    if url:
                        response += (
                        f'🔗 <a href="{url}" target="_blank">'
                        "View Notification</a>\n"
                        )
                    response += "\n"
                response += (
                       "🌐 <b>Source:</b> "
                       '<a href="https://www.cusrinagar.edu.in/Notification/Notification" '
                       'target="_blank">Official CUS Notification Section</a>'
                )
                return response

            # LATEST RESULTS
            if result_type == "results":
                response = (
                    "📊 <b>Latest Results – "
                    "Cluster University Srinagar</b>\n\n"
                )
                for item in items:
                    item_type, title, item_date, url = item
                    response += f"📌 <b>{title}</b>\n"
                    if item_date:
                        try:
                            display_date = datetime.strptime(
                                item_date,
                                "%Y-%m-%d"
                            ).strftime("%d-%B-%Y")
                        except ValueError:
                            display_date = item_date
                        response += f"📅 {display_date}\n"

                    if url:
                        response += (
                            f'🔗 <a href="{url}" target="_blank">'
                            "View Result</a>\n"
                        )
                    response += "\n"
                response += (
                    "🌐 <b>Source:</b> "
                    '<a href="https://www.cusrinagar.edu.in/Result/ResultNotification" '
                    'target="_blank">Official CUS Results Section</a>'
                )
                return response

        college, title, url, chunk, chunk_no = web_result

        return f"""
🌐 <b>{title}</b>

{chunk[:1500]}

<b>Source:</b>
<a href="{url}" target="_blank">{url}</a>
"""

    return (
        "I couldn't find the requested information in the "
        "available official documents."
    )