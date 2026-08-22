import re

from chatbot.programme_search import (
    search_programmes,
    get_last_programme,
    search_programme_list,
    search_subject_overview,
    search_all_matching_programmes
)
from chatbot.general_admission import get_general_admission_response
# spellcheck
from chatbot.spellcheck import find_closest_subject
from chatbot.query_intents import *
def programme_not_found_response():
    return (
        "I'm sorry, I couldn't find a matching programme "
        "for your query. Please check the programme name "
        "or subject and try again."
    )

def programme_response(question):
    print("Programme Module Called")
    print("PROGRAMME RESPONSE QUESTION:", repr(question))
    # GENERAL ADMISSION INFORMATION
    general_admission_response = (
        get_general_admission_response(question)
    )
    if general_admission_response:
        return general_admission_response
    
    question = question.lower().strip()  
    college_query = (
        "which college" in question
        or "which colleges" in question
        or "what college" in question
        or "what colleges" in question
        or "colleges offering" in question
        or "colleges offer" in question
        or "colleges have" in question
        or "college has" in question
        or "where can i study" in question
        or "where to study" in question
        or "where can i do" in question
    )

    department_query = (
        "which department" in question
        or "what department" in question
        or "which dept" in question
        or "what dept" in question
        or "department offers" in question
        or "department offer" in question
    )


    #NORMALIZE COMMON WORDING
    question = question.replace("programs", "programmes")
    question = question.replace("program", "programme")

    #LEVEL-ONLY LIST QUESTIONS
    level_only_query = False

    level_patterns = [
        "pg programmes",
        "pg programme",
        "postgraduate programmes",
        "postgraduate programme",
        "post graduate programmes",
        "post graduate programme",

        "ug programmes",
        "ug programme",
        "undergraduate programmes",
        "undergraduate programme",
        "under graduate programmes",
        "under graduate programme",

        "integrated programmes",
        "integrated programme"
    ]

    if question in level_patterns:
        level_only_query = True

    if (
        ("pg" in question or "postgraduate" in question or "post graduate" in question)
        and "programme" in question
    ):
        level_only_query = True

    if (
        ("ug" in question or "undergraduate" in question or "under graduate" in question)
        and "programme" in question
    ):
        level_only_query = True

    if (
        "integrated" in question
        and "programme" in question
    ):
        level_only_query = True

    #HANDLE LEVEL-ONLY LIST QUERY
    if level_only_query:

        programmes = search_programme_list(question)

        if not programmes:
            return "No matching programmes found."

        answer = (
            f"📚 <b>Available Programmes ({len(programmes)})</b>\n\n"
        )

        for p in programmes:

            programme_name = (
                p["programme"] or ""
            ).strip()

            specialization = (
                p["specialization"] or ""
            ).strip()

            college = (
                p["college"] or ""
            ).strip()

            line = f"📘 <b>{programme_name}"

            if specialization:
                line += f" - {specialization}"

            line += "</b>\n"

            if college:
                line += f"🏛 {college}\n\n"

            answer += line

        return answer
        # COLLEGE QUESTIONS
    if college_query:

        matching_programmes = search_all_matching_programmes(
            question
        )

        print("\nMATCHING PROGRAMMES:")

        for p in matching_programmes:
            print(
                "PROGRAMME =", p["programme"],
                "| SPECIALIZATION =", p["specialization"],
                "| COLLEGE =", p["college"]
            )

        if not matching_programmes:
            return programme_not_found_response()
            # return (
            #     "I'm sorry, I couldn't find any "
            #     "matching programme."
            # )

        colleges = []
        for p in matching_programmes:

            college = (
                p["college"] or ""
            ).strip()

            if college and college not in colleges:
                colleges.append(college)

        programme = matching_programmes[0]

        programme_name = (
            programme["programme"] or ""
        ).strip()

        specialization = (
            programme["specialization"] or ""
        ).strip()

        display_programme = programme_name

        if specialization and specialization.lower() not in [
            "general",
            "regular",
            "none"
        ]:
            display_programme += (
                f" - {specialization}"
            )

        answer = (
            f"<b>Colleges Offering "
            f"{display_programme}:</b>\n\n"
        )

        for college in colleges:
            answer += f"🏛 {college}\n"

        return answer

    #NORMAL LIST QUESTIONS
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
        "all programmes",
        "all programs",
        "available in",
        "programmes",
        "programme",
        "programs",
        "program"
    ]
 
    is_list_query = (
        any(word in question for word in list_keywords)
        and not college_query
        and not department_query
    )

    if is_list_query:
        programmes = search_programme_list(
            question
        )
        if not programmes:
            return programme_not_found_response()
            # return "No matching programmes found."

        answer = (
            f"📚 <b>Available Programmes "
            f"({len(programmes)})</b>\n\n"
        )

        for p in programmes:
            programme_name = (
                p["programme"] or ""
            ).strip()

            specialization = (
                p["specialization"] or ""
            ).strip()

            college = (
                p["college"] or ""
            ).strip()

            line = (
                f"📘 <b>{programme_name}"
            )

            if specialization:
                line += (
                    f" - {specialization}"
                )

            line += "</b>\n"

            if college:
                line += (
                    f"🏛 {college}\n\n"
                )
            answer += line
        return answer

    #GENERAL SUBJECT QUERY
    level_words = {
        "bsc", "msc", "ba", "ma", "bca", "mca",
        "bba", "mba", "bcom", "mcom",
        "bed", "med", "integrated"
    }
    question_words = set(question.split())

    specific_programme_query = any(
        word in question_words
        for word in level_words
    )
    generic_subject_query = (
      question == "it"
      #spellcheck
      or question.startswith("what is ")
      or question.startswith("what are ")
      or question.startswith("information on ")

      or question.startswith( "tell me about")
      or question.startswith("about") 
      or question.startswith("information about")
    )

    if generic_subject_query and not specific_programme_query:
        subject_query = question
        subject_query = re.sub(
           r"^(what is|what are|information on|tell me about|information about|about)\s+",
           "",
            subject_query
        ).strip()

        #spellcheck
        print(
            "GENERAL SUBJECT QUERY:",
            subject_query
        )
        print(
            "SUBJECT OVERVIEW SEARCH:",
             repr(subject_query)
        )
      
        subject_result = search_subject_overview(
            subject_query
        )

        #spellcheck
        if subject_result is None:

            matched_subject, _ = find_closest_subject(
                    subject_query,
                    # threshold=0.70
                )
        
            if matched_subject:

                subject_result = search_subject_overview(
                    matched_subject
                )
            #yehan tak

        if subject_result:
         return (
            f"📘 <b>{subject_result['subject'].title()}</b>\n\n"
            f"{subject_result['overview']}"
         )

    programme = search_programmes(question)
    if programme is None:
        return programme_not_found_response()

    # DEPARTMENT QUERY
    if department_query:
        return (
          f"📘 <b>{programme['programme']}"
          f"{' - ' + programme['specialization'] if programme['specialization'] else ''}</b>\n\n"
          f"<b>Department:</b> {programme['department']}"
        )

    #SINGLE PROGRAMME RESPONSE
    response = [
        f"📘 <b>{programme['programme']}"
    ]

    if programme["specialization"]:
        response[0] += (
            f" - {programme['specialization']}"
        )

    response[0] += "</b>\n"
    if contains_any(question, INTAKE):
        response.append(
            f"<b>Intake:</b> "
            f"{programme['intake']}"
        )

    if contains_any(question, ELIGIBILITY):
        response.append(
            f"<b>Eligibility:</b> "
            f"{programme['eligibility']}"
        )

    if contains_any(question, FEE):
        response.append(
            f"<b>Fee:</b> "
            f"{programme['fee']}"
        )

    if contains_any(question, DURATION):
        response.append(
            f"<b>Duration:</b> "
            f"{programme['duration']}"
        )
    
    if contains_any(question, DEPARTMENT):
        response.append(
            f"<b>Department:</b> "
            f"{programme['department']}"
        )

    if contains_any(question, ADMISSION):
        response.append(
            f"<b>Admission Process:</b> "
            f"{programme['admission_process']}"
        )

    if contains_any(question, SELECTION):
        response.append(
            f"<b>Selection Process:</b> "
            f"{programme['selection_process']}"
        )
    if len(response) > 1:
        return "\n\n".join(response)

    return f"""
📘 {programme['programme']}{"-" + programme['specialization'] if programme['specialization'] else ""}

Programme Level: {programme['level']}

College: {programme['college']}

Department: {programme['department']}

Duration: {programme['duration']}

Eligibility: {programme['eligibility']}

Intake: {programme['intake']}

Fee: {programme['fee']}

Admission Process: {programme['admission_process']}

Selection Process: {programme['selection_process']}

Overview: {programme['subject_overview'] or programme['overview']}

School: {programme['school']}

Campus: {programme['campus']}
"""