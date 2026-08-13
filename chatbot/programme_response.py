import re

from chatbot.programme_search import (
    search_programmes,
    get_last_programme,
    search_programme_list,
    search_subject_overview,
    search_all_matching_programmes
)
from chatbot.query_intents import *

def programme_response(question):
    print("Programme Module Called")
    print("PROGRAMME RESPONSE QUESTION:", repr(question))
    question = question.lower().strip()

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

    #COLLEGE QUESTIONS
    if (
        "which college" in question
        or "which colleges" in question
    ):

        programmes = search_programme_list(question)

        print(
            "COLLEGE QUERY RESULTS:",
            len(programmes)
        )

        if not programmes:
            return "No matching programmes found."

        #UNIQUE COLLEGES
        colleges = []
        seen_colleges = set()

        for p in programmes:

            college = (
                p["college"] or ""
            ).strip()

            if not college:
                continue

            # Normalize whitespace
            college = " ".join(
                college.split()
            )

            # Normalize common college-name variations
            college_key = college.lower()

            if college_key == "government college for women":
                display_college = "Govt. College for Women"

            elif college_key == "govt. college for women":
                display_college = "Govt. College for Women"

            elif college_key == "abdul ahad azad memorial degree college":
                display_college = "Abdul Ahad Azad Memorial College"

            else:
                display_college = college

            key = display_college.lower()

            if key not in seen_colleges:

                seen_colleges.add(key)
                colleges.append(display_college)

        print(
            "FINAL COLLEGES:",
            colleges
        )

        if not colleges:
            return "No matching colleges found."

        #PROGRAMME TITLES
        programme_titles = []
        for p in programmes:

            programme_name = (
                p["programme"] or ""
            ).strip()

            specialization = (
                p["specialization"] or ""
            ).strip()

            if specialization:

                title = (
                    f"{programme_name} - "
                    f"{specialization}"
                )
            else:

                title = programme_name
            if title not in programme_titles:
                programme_titles.append(title)

        #HEADING
        if len(programme_titles) == 1:
            answer = (
                f"<b>Colleges Offering "
                f"{programme_titles[0]}:</b>\n\n"
            )
        else:
            answer = (
                "<b>Colleges Offering the Matching "
                "Programmes:</b>\n\n"
            )

        #COLLEGE LIST
        for college in colleges:

            answer += (
                f"🏛 {college}\n"
            )

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

    is_list_query = any(
        word in question
        for word in list_keywords
    )

    if is_list_query:
        programmes = search_programme_list(
            question
        )
        if not programmes:
            return "No matching programmes found."

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
      or question.startswith( "tell me about")
      or question.startswith("about") 
      or question.startswith("information about")
    )

    if generic_subject_query and not specific_programme_query:
        subject_query = question
        subject_query = re.sub(
           r"^(tell me about|information about|about)\s+",
           "",
            subject_query
        ).strip()
      
        subject_result = search_subject_overview(
            subject_query
        )

        if subject_result:
         return (
            f"📘 <b>{subject_result['subject'].title()}</b>\n\n"
            f"{subject_result['overview']}"
         )

    programme = search_programmes(question)
    college_query = (
        "which college" in question
        or "which colleges" in question
        or "what college" in question
        or "what colleges" in question
        or "colleges offering" in question
        or "colleges offer" in question
    )
    if college_query:
        matching_programmes = search_all_matching_programmes(question)
        if not matching_programmes:
          return (
           "I'm sorry, I couldn't find any "
            "matching programme."
        )
        programme = matching_programmes[0]
    else:
        programme = search_programmes(question)
        if programme is None:
          return (
            "I'm sorry, I couldn't find any "
            "matching programme."
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
    if college_query:
     colleges = []
     for p in matching_programmes:
      college = (
        p["college"] or ""
      ).strip()

      if college and college not in colleges:
        colleges.append(college)

     if len(colleges) > 1:
      response.append(
        "<b>Colleges Offering:</b>\n" +
        "\n".join(
            f"🏛 {college}"
            for college in colleges
        )
     )

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

    # if contains_any(question, COLLEGE):
    #     if len(colleges) > 1:
    #      response.append(
    #         "<b>Colleges:</b>\n" +
    #         "\n".join(
    #             f"🏛 {college}"
    #             for college in colleges   
    #         )
    #     )
    #     elif len(colleges) == 1:
    #         response.append(
    #             f"<b>College:</b> {colleges[0]}"
            # )
    
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