from chatbot.programme_search import search_programmes, get_last_programme
from chatbot.query_intents import *

def programme_response(question):
    programme = search_programmes(question)

    if programme is None:
        programme = get_last_programme()
    print("Current Programme:", programme["programme_name"] if programme else "None")

    if programme is None:
        return "I'm sorry, I couldn't find any programme matching your query. Please try asking about a specific programme."
    question = question.lower()
    response = []
    response.append(f"📘 <b>{programme['programme_name']}</b>\n")

    #Specific Information
    if contains_any(question, INTAKE):
        response.append(
            f"<b>Intake:</b> {programme['intake']}"
        )
    if contains_any(question, ELIGIBILITY):
        response.append(
            f"<b>Eligibility:</b> {programme['eligibility']}"
        )
    if contains_any(question, FEE):
        response.append(
            f"<b>Fee:</b> {programme['fee']}"
        )
    if contains_any(question, DURATION):
        response.append(
            f"<b>Duration:</b> {programme['duration']}"
        )
    if contains_any(question, COLLEGE):
        response.append(
            f"<b>College:</b> {programme['college']}"
        )
    if contains_any(question, DEPARTMENT):
        response.append(
            f"<b>Department:</b> {programme['department']}"
        )
    if contains_any(question, ADMISSION):
        response.append(
            f"<b>Admission Process:</b> {programme['admission_process']}"
        )
    if contains_any(question, SELECTION):
        response.append(
            f"<b>Selection Process:</b> {programme['selection_process'] or 'Official information not available.'}"
        )
    #If user asked one or more specific things
    if len(response) > 1:
        return "\n\n".join(response)
    return f"""
📘 <b>{programme['programme_name']}</b>

<b>Programme Level:</b> {programme['programme_level'] or "Official information not available."}

<b>College:</b> {programme['college'] or "Official information not available."}

<b>Department:</b> {programme['department'] or "Official information not available."}

<b>Duration:</b> {programme['duration'] or "Official information not available."}

<b>Eligibility:</b> {programme['eligibility'] or "Official information not available."}

<b>Intake:</b> {programme['intake'] or "Official information not available."}

<b>Fee:</b> {programme['fee'] or "Official information not available."}

<b>Admission Process:</b> {programme['admission_process'] or "Official information not available."}

<b>Selection Process:</b> {programme['selection_process'] or "Official information not available."}

<b>Overview:</b> {programme['overview'] or "Official information not available."}
"""