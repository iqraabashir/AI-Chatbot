from chatbot.programme_search import (
    search_programmes,
    get_last_programme,
    search_programme_list
)
from chatbot.query_intents import *


def programme_response(question):
    print("Programme Module Called")
    question = question.lower()
    if "which college" in question or "which colleges" in question:
        programmes = search_programme_list(question)
        if not programmes:
            return "No matching programmes found."
        colleges = []
        for p in programmes:
            if p["college"] not in colleges:
                colleges.append(p["college"])
        programme_name = programmes[0]["programme"]
        specialization = programmes[0]["specialization"]
        if specialization:
            title = f"{programme_name} - {specialization}"
        else:
            title = programme_name
        answer = f"<b>Colleges Offering {title} :</b>\n\n"
        for c in colleges:
            answer += f"🏛 {c}\n"
        return answer

    list_keywords = [
        "list",
        "show",
        "display",
        "available",
        "offered",
        "offer",
        "offers",
        "programmes offered",
        "courses offered",
        "provides",
        "provide",
        "programmes provided",
        "courses provided",
        "which college",
        "which colleges",
        "all programmes",
        "all programs",
        "available in"
    ]

    is_list_query = any(word in question for word in list_keywords)

    #LIST QUERIES

    if is_list_query:

        programmes = search_programme_list(question)

        if not programmes:
            return "No matching programmes found."

        answer = f"📚 <b>Available Programmes ({len(programmes)})</b>\n\n"

        for p in programmes:

            if "which college" in question or "which colleges" in question:
                line = f"🏛 {p['college']}\n"
                line += f"📘 {p['programme']}"
            else:
                line = f"📘 {p['programme']}"
                # change line += f"\n🏛 {p['college']}\n"

            if p["specialization"]:
                line += f" - {p['specialization']}"

            line += f"\n🏛 {p['college']} \n"

            answer += line

        return answer

    #SINGLE PROGRAMME
    programme = search_programmes(question)
    if programme is None:
        programme = get_last_programme()

    if programme is None:
        return "I'm sorry, I couldn't find any matching programme."

    response = [f"📘 <b>{programme['programme']}"]

    if programme["specialization"]:
        response[0] += f" - {programme['specialization']}"

    response[0] += "</b>\n"

    if contains_any(question, INTAKE):
        response.append(f"<b>Intake:</b> {programme['intake']}")

    if contains_any(question, ELIGIBILITY):
        response.append(f"<b>Eligibility:</b> {programme['eligibility']}")

    if contains_any(question, FEE):
        response.append(f"<b>Fee:</b> {programme['fee']}")

    if contains_any(question, DURATION):
        response.append(f"<b>Duration:</b> {programme['duration']}")

    if contains_any(question, COLLEGE):
        response.append(f"<b>College:</b> {programme['college']}")

    if contains_any(question, DEPARTMENT):
        response.append(f"<b>Department:</b> {programme['department']}")

    if contains_any(question, ADMISSION):
        response.append(f"<b>Admission Process:</b> {programme['admission_process']}")

    if contains_any(question, SELECTION):
        response.append(f"<b>Selection Process:</b> {programme['selection_process']}")

    if len(response) > 1:
        return "\n\n".join(response)

    return f"""
📘 <b>{programme['programme']}{" - " + programme['specialization'] if programme['specialization'] else ""}</b>

<b>Programme Level:</b> {programme['level']}

<b>College:</b> {programme['college']}

<b>Department:</b> {programme['department']}

<b>Duration:</b> {programme['duration']}

<b>Eligibility:</b> {programme['eligibility']}

<b>Intake:</b> {programme['intake']}

<b>Fee:</b> {programme['fee']}

<b>Admission Process:</b> {programme['admission_process']}

<b>Selection Process:</b> {programme['selection_process']}

<b>Overview:</b> {programme['overview']}

<b>School:</b> {programme['school']}

<b>Campus:</b> {programme['campus']}
"""