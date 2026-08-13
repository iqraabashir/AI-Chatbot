import sqlite3

DATABASE_NAME = "chatbot/knowledge.db"


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

    question = question.lower().strip()

    best = None
    best_score = 0

    for record in records:

        field = (record["field"] or "").lower()
        value = (record["value"] or "").lower()

        score = 0

        # Exact field match
        if field in question:
            score += 100

        # Words from field
        for word in field.split():
            if len(word) > 2 and word in question:
                score += 10

        # Words from value
        for word in value.split():
            if len(word) > 3 and word in question:
                score += 1

        if score > best_score:
            best_score = score
            best = record

    return best


def university_response(question):

    record = search_university_info(question)

    if record is None:
        return None

    field = record["field"]
    value = record["value"]
    source = record["source"]
    url = record["url"]

    response = (
        f"🏛 <b>Cluster University Srinagar</b>\n\n"
        f"<b>{field}:</b> {value}"
    )

    if url:
        response += (
            f'\n\n<b>Source:</b> '
            f'<a href="{url}" target="_blank">{source or "Official University Website"}</a>'
        )

    return response



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