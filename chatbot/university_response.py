import sqlite3
import re
from chatbot.aliases import UNIVERSITY_ALIASES

DATABASE_NAME = "chatbot/knowledge.db"
def normalize_university_question(question):

    question = (question or "").lower().strip()

    # Remove punctuation
    question = re.sub(r"[^a-z0-9\s-]", " ", question)

    # Normalize whitespace
    question = re.sub(r"\s+", " ", question).strip()

    # Sort aliases from longest to shortest
    for alias, field in sorted(
        UNIVERSITY_ALIASES.items(),
        key=lambda x: len(x[0]),
        reverse=True
    ):
        pattern = rf"\b{re.escape(alias)}\b"

        question = re.sub(
            pattern,
            field,
            question
        )

    return re.sub(r"\s+", " ", question).strip()


def search_university_info(question):

    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM university_info
    """)

    records = cursor.fetchall()
    conn.close()
    original_question = (question or "").lower().strip()
    normalized_question = normalize_university_question(
        original_question
    )
    print(
        "UNIVERSITY SEARCH QUESTION:",
        repr(normalized_question)
    )


    best = None
    best_score = 0

    for record in records:

        field = (record["field"] or "").lower().strip()
        value = (record["value"] or "").lower().strip()

        score = 0

        # Exact field match
        if field in normalized_question:
            score += 200

        if field in UNIVERSITY_ALIASES.values():

            if field in normalized_question:
                score += 300

        # Words from field
        for word in field.split():
            if len(word) > 2 and word in normalized_question:
                score += 20

        # Words from value
        for word in value.split():
            if len(word) > 4 and word in normalized_question:
                score += 1

        if score > best_score:
            best_score = score
            best = record
    print(
        "UNIVERSITY BEST FIELD:",
        best["field"] if best else None
    )

    print(
        "UNIVERSITY SCORE:",
        best_score
    )

    return best

def search_all_university_info(question, field_name):

    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM university_info
        WHERE LOWER(field) = LOWER(?)
        ORDER BY university_info_id
    """, (field_name,))

    records = cursor.fetchall()

    conn.close()

    return records
def university_response(question):
    normalized_question = normalize_university_question(question)

    if "constituent colleges" in normalized_question:

        records = search_all_university_info(
            question,
            "College 1"
        )

        # If your database has College 1, College 2... College 5
        # fetch all constituent-college records directly.
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM university_info
            WHERE LOWER(field) LIKE 'college %'
            ORDER BY university_info_id
        """)

        records = cursor.fetchall()
        conn.close()

        if records:

            response = [
                "🏛 <b>Cluster University Srinagar</b>",
                "<b>Constituent Colleges:</b>"
            ]

            for record in records:
                response.append(
                    f"🏛 {record['value']}"
                )

            return "\n\n".join(response)

    record = search_university_info(question)

    if record is None:
        return None

    field = record["field"]
    value = record["value"]
    source = (
        record["source"]
        if "source" in record.keys()
        else""
    )

    url = (
        record["url"]
        if "url" in record.keys()
        else ""
    )

    email = ""

    if "email" in record.keys():
        email = record["email"] or ""
       

    response = [
        "🏛 <b>Cluster University Srinagar</b>",
        f"<b>{field}:</b> {value}"
    ]
    if email:
        response.append(
            f'<b>Email:</b> '
            f'<a href="mailto:{email}">{email}</a>'
        )

    if url:
        response.append(
            f'<b>Source:</b> '
            f'<a href="{url}" target="_blank">'
            f'{source or "Official University Website"}'
            f'</a>'
        )

    return "\n\n".join(response)



# from chatbot.university_search import (
#     search_university,
#     get_last_university_record
# )


# def university_response(question):

#     record = search_university(question)

#     if record is None:
#         record = get_last_university_record()

#     if record is None:
#         return None

#     q = (question or "").lower()

#     field = (
#         record["field"] or ""
#     ).lower()

#     value = (
#         record["value"] or ""
#     )

#     source = (
#         record["source"] or ""
#     )

#     url = (
#         record["url"] or ""
#     )

#     email = (
#         record["email"] or ""
#     )

#     # UNIVERSITY NAME
#     if (
#         "university name" in field
#         or "name of university" in q
#     ):
#         return (
#             f"🏛 <b>University Name:</b> {value}"
#         )

#     # ESTABLISHED
#     elif (
#         "established" in field
#         or "establishment" in q
#     ):
#         return (
#             f"📅 <b>Established:</b> {value}"
#         )

#     # UNIVERSITY TYPE
#     elif (
#         "university type" in field
#         or "type of university" in q
#     ):
#         return (
#             f"🏛 <b>University Type:</b> {value}"
#         )

#     # ESTABLISHED UNDER
#     elif (
#         "established under" in field
#         or "which act" in q
#         or "under which act" in q
#     ):
#         return (
#             f"📜 <b>Established Under:</b> {value}"
#         )

#     # FUNDING
#     elif (
#         "funding scheme" in field
#         or "funding" in q
#     ):
#         return (
#             f"💰 <b>Funding Scheme:</b> {value}"
#         )

#     # HEADQUARTERS
#     elif (
#         "headquarters" in field
#         or "headquarter" in q
#     ):
#         return (
#             f"📍 <b>Headquarters:</b> {value}"
#         )

#     # PURPOSE
#     elif "purpose" in field:
#         return (
#             f"🎯 <b>Purpose:</b> {value}"
#         )

#     # VISION
#     elif "vision" in field:
#         return (
#             f"🔭 <b>Vision:</b> {value}"
#         )

#     # MISSION
#     elif "mission" in field:
#         return (
#             f"🎓 <b>Mission:</b> {value}"
#         )

#     # CHANCELLOR
#     elif "chancellor" in field:
#         response = (
#             f"👤 <b>Chancellor:</b> {value}"
#         )

#         if email:
#             response += (
#                 f"\n📧 <b>Email:</b>"
#                 f'<a href="mailto:{email}>"{email}</a>'
#             )

#         return response

#     # VICE CHANCELLOR
#     elif "vice chancellor" in field:
#         response = (
#             f"👤 <b>Vice Chancellor:</b> {value}"
#         )

#         if email:
#             response += (
#                 f"\n📧 <b>Email:</b>"
#                 f'<a href="mailto:{email}>"{email}</a>'
#             )

#         return response

#     # PRO CHANCELLOR
#     elif "pro chancellor" in field:
#         response = (
#             f"👤 <b>Pro Chancellor:</b> {value}"
#         )

#         if email:
#             response += (
#                 f"\n📧 <b>Email:</b>"
#                 f'<a href="mailto:{email}>"{email}</a>'
#             )

#         return response

#     # REGISTRAR
#     elif "registrar" in field:
#         response = (
#             f"👤 <b>Registrar:</b> {value}"
#         )

#         if email:
#             response += (
#                 f"\n📧 <b>Email:</b>"
#                 f'<a href="mailto:{email}>"{email}</a>'
#             )

#         return response

#     # CONTROLLER OF EXAMINATIONS
#     elif "controller of examinations" in field:
#         response = (
#             f"📝 <b>Controller of Examinations:</b> "
#             f"{value}"
#         )

#         if email:
#             response += (
#                 f"\n📧 <b>Email:</b>"
#                 f'<a href="mailto:{email}>"{email}</a>'
#             )

#         return response

#     # CONSTITUENT COLLEGES
#     elif "college" in field.lower():

#         return (
#             f"🏛 <b>{field.title()}:</b> {value}"
#         )

#     # WEBSITE
#     elif "website" in field:

#         return (
#             f"🌐 <b>Official Website:</b> "
#             f'<a href="{value}" target="_blank">'
#             f"Visit Official Website</a>"
#         )

#     # EMAIL
#     elif email and (
#         "email" in q
#         or "email" in field
#     ):

#         return (
#             f"\n📧 <b>Email:</b>"
#             f'<a href="mailto:{email}>"{email}</a>'
#         )

#     # FALLBACK
#     else:

#         response = (
#             f"🏛 <b>{field.title()}</b>\n"
#             f"{value}"
#         )

#         if email:
#             response += (
#                 f"\n📧 <b>Email:</b>"
#                 f'<a href="mailto:{email}>"{email}</a>'
#             )

#         if url:
#             response += (
#                 f'\n🌐 <b>Website:</b> '
#                 f'<a href="{url}" target="_blank">Visit Official Website</a>'
#             )

#         return response