import sqlite3
import re
from chatbot.aliases import COLLEGE_ALIASES, PROGRAMME_ALIASES

from matplotlib.pylab import long

LAST_PROGRAMME = None
DATABASE_NAME = "chatbot/knowledge.db"


def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# def search_programmes(user_question):
#     conn = sqlite3.connect(DATABASE_NAME)
#     conn.row_factory = sqlite3.Row
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM academic_programmes")
#     programmes = cursor.fetchall()
#     conn.close()
#     question = user_question.lower()

#     question_words = set(question.split())
#     question = " "+question+" "
#     for short,full in COLLEGE_ALIASES.items():
#         question = question.replace(f"{short}", f"{full}")
#     for short,full in PROGRAMME_ALIASES.items():
#         question = question.replace(f"{short}", f"{full}")
#     question = (question.strip())
#     best_match = None
#     best_score = -1
#     for programme in programmes:
#         score = 0

#         print("...............")
#         print(name := programme["programme"])

#         programme_name = (programme["programme"] or "").lower().strip()
#         specialization = (programme["specialization"] or "").lower().strip()
#         college = (programme["college"] or "").lower().strip()
#         department = (programme["department"] or "").lower().strip()
#         level = (programme["level"] or "").lower().strip()
#         full_name = f"{programme_name} {specialization}".strip()

#         #Exact full programme
#         if full_name in question:
#             score += 100

#         #Programme 
#         if programme_name in question_words:
#             score += 60

#         #Specialization
#         if specialization and specialization in question:
#             score += 40

#         #College
#         if college and college in question:
#             score += 20

#         #Department
#         if department and department in question:
#             score += 15

#         #Level
#         question_words = set(question.split())

#         UG = {"ba", "bsc", "bca", "bba", "bcom"}
#         PG = {"ma", "msc", "mca", "mba", "mcom"}

#         if "integrated" in question_words:
#          if level == "integrated":
#           score += 20

#         elif question_words & PG:
#          if level == "pg":
#           score += 20

#         elif question_words & UG:
#          if level == "ug":
#           score += 20

#         #Individual words
#         for word in full_name.split():
#             if len(word) > 2 and word in question:
#                 score += 5

#         print(score)       
#         if score > best_score:
#             best_score = score
#             best_match = programme
#     global LAST_PROGRAMME
#     if best_match:
#         LAST_PROGRAMME = best_match
#     return best_match
def search_programmes(user_question):

    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM academic_programmes")
    programmes = cursor.fetchall()

    conn.close()

    from chatbot.aliases import COLLEGE_ALIASES, PROGRAMME_ALIASES

    question = " " + user_question.lower() + " "

    # Expand aliases
    for short, full in COLLEGE_ALIASES.items():
        question = question.replace(f" {short} ", f" {full} ")

    for short, full in PROGRAMME_ALIASES.items():
        question = question.replace(f" {short} ", f" {full} ")

    question = question.strip()
    question_words = set(question.split())

    UG = {"ba", "bsc", "bca", "bba", "bcom", "bed"}
    PG = {"ma", "msc", "mca", "mba", "mcom", "med"}

    best_match = None
    best_score = -1

    for programme in programmes:
        score = 0

        programme_name = (programme["programme"] or "").lower().strip()
        specialization = (programme["specialization"] or "").lower().strip()
        college = (programme["college"] or "").lower().strip()
        department = (programme["department"] or "").lower().strip()
        school = (programme["school"] or "").lower().strip()
        level = (programme["level"] or "").lower().strip()
        full_name = f"{programme_name} {specialization}".strip()

        # Exact full programme
        if full_name and full_name in question:
            score += 100

        # Programme Name
        if programme_name in question_words:
            score += 60

        # Specialization
        if specialization and specialization in question:
            score += 45

        # College
        if college and college in question:
            score += 25

        # Department
        if department and department in question:
            score += 20

        # School
        if school and school in question:
            score += 15

        #Level Matching
        if "integrated" in question_words:
            if level == "integrated":
                score += 40
            else:
                score -= 100
        elif question_words & PG:
            if level == "pg":
                score += 30
            else:
                score -= 40
        elif question_words & UG:
            if level == "ug":
                score += 30
            else:
                score -= 40

        # Individual words
        for word in full_name.split():
            if len(word) < 3:
                continue
            if word in question_words:
                score += 6

        if specialization:
            spec_words = specialization.split()
            if all(word in question_words for word in spec_words):
                score += 20

        if score > best_score:
            best_score = score
            best_match = programme

    global LAST_PROGRAMME

    if best_match:
        LAST_PROGRAMME = best_match

    return best_match


def get_last_programme():
    return LAST_PROGRAMME

def search_programme_list(question):
    question = question.lower()
    
    question = " "+question+" "
    for short,full in COLLEGE_ALIASES.items():
        question = question.replace(f"{short}", f"{full}")

    for short,full in PROGRAMME_ALIASES.items():
        question = question.replace(f"{short}", f"{full}")
    question = question.strip()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM academic_programmes")
    programmes = cursor.fetchall()
    conn.close()

    results = []

    for programme in programmes:
        programme_name = (programme["programme"] or "").lower()
        specialization = (programme["specialization"] or "").lower()
        department = (programme["department"] or "").lower()
        college = (programme["college"] or "").lower()
        school = (programme["school"] or "").lower()
        level = (programme["level"] or "").lower()
        if "integrated" in question:
            if programme_name != "integrated msc" and level != "integrated":
                continue
        elif "msc" in question:
            if programme_name != "msc":
                continue
        elif "ma" in question:
            if programme_name != "ma":
                continue
        elif "mca" in question:
            if programme_name != "mca":
                continue
        elif "mba" in question:
            if programme_name != "mba":
                continue
        elif "bsc" in question:
            if programme_name != "bsc":
                continue
        elif "ba" in question:
            if programme_name != "ba":
                continue
        elif "bba" in question:
            if programme_name != "bba":
                continue
        elif "bcom" in question:
            if programme_name != "bcom":
                continue
        
        programme_type = (programme["programme_type"] or "").lower()

        search_text = " ".join([
            programme_name,
            specialization,
            department,
            college,
            school,
            level,
            programme_type
        ]).lower()
        search_words = set(search_text.split())

        keywords = [
         w.lower() for w in re.findall(r"[a-zA-Z0-9]+", question)
         if len(w) > 2 and w.lower() not in {
           "list",
           "show",
           "display",
           "available",
           "offer",
           "offers",
           "offered",
           "provide",
           "provides",
           "which",
           "college",
           "colleges",
           "programme",
           "programmes",
           "program",
           "programs",
           "course",
           "courses",
           "all",
           "can",
           "i",
           "study",
           "where",
           "to",
           "in",
           "for",
           "the",
           "of"
        }
    ]
        score = 0
        for word in keywords:
            if word in search_words:
                score += 1
        matched = score == len(keywords)
        if "physics" in question:
            print("---------")
            print(search_text)
            print(keywords)
            print(score)
            print(matched)

        if matched:
          results.append(programme)

    results.sort(
        key=lambda x: (
            x["programme"] or "",
            x["specialization"] or "",
            x["college"] or ""
        )
    )
    return results