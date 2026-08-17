import sqlite3
import re

from chatbot.aliases import COLLEGE_ALIASES, PROGRAMME_ALIASES

LAST_PROGRAMME = None
DATABASE_NAME = "chatbot/knowledge.db"

def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def normalize_question(text):
    text = (text or "").lower().strip()
    # new bed
    text = re.sub(r"\bb\s*\.?\s*\.?\s*e\s*\.?\s*d\b", "bed", text)
    text = re.sub(r"\bm\s*\.?\s*\.?\s*e\s*\.?\s*d\b", "med", text)
    text = re.sub(r"[^a-z0-9\s&-]", " ", text)
    for short, full in sorted(
        COLLEGE_ALIASES.items(),
        key=lambda x: len(x[0]),
        reverse=True
    ):
        text = re.sub(
            rf"\b{re.escape(short.lower())}\b",
            full.lower(),
            text
        )

    for short, full in sorted(
        PROGRAMME_ALIASES.items(),
        key=lambda x: len(x[0]),
        reverse=True
    ):
        text = re.sub(
            rf"\b{re.escape(short.lower())}\b",
            full.lower(),
            text
        )

    replacements = {
        "bachelor of computer applications": "bca",
        "master of science": "msc",
        "master of arts": "ma",
        "master of computer applications": "mca",
        "master of business administration": "mba",
        "master of commerce": "mcom",
        "master of education": "med",
        "bachelor of science": "bsc",
        "bachelor of arts": "ba",
        "bachelor of commerce": "bcom",
        "bachelor of business administration": "bba",
        "bachelor of education": "bed",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)
    return re.sub(r"\s+", " ", text).strip()

def get_words(text):
    return set(
        re.findall(
            r"[a-z0-9]+(?:-[a-z0-9]+)*",
            text.lower()
        )
    )

UG = {
    "ba",
    "bsc",
    "bca",
    "bba",
    "bcom",
    "bed"
}

PG = {
    "ma",
    "msc",
    "mca",
    "mba",
    "mcom",
    "med"
}

def get_all_programmes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM academic_programmes"
    )
    programmes = cursor.fetchall()
    conn.close()
    return programmes

def search_subject_overview(subject):
    subject = normalize_question(subject).strip()

    if subject == "it":
        subject = "information technology"

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM academic_programmes
        WHERE LOWER(TRIM(specialization)) = ?
           OR LOWER(TRIM(department)) = ?
        ORDER BY id
        LIMIT 1
    """, (
        subject.lower(),
        subject.lower()
    ))

    programme = cursor.fetchone()
    conn.close()

    if programme is None:
        return None

    overview = (
        programme["subject_overview"] or ""
    ).strip()

    if not overview:
        return None

    return {
        "subject": subject,
        "overview": overview
    }

def search_all_matching_programmes(user_question):
    question = normalize_question(user_question)
    words = get_words(question)
    programmes = get_all_programmes()
    matches = []
    for p in programmes:
        programme_name = normalize_programme_name(
            p["programme"] or ""
        )
        specialization = normalize_question(
            p["specialization"] or ""
        )
        department = normalize_question(
            p["department"] or ""
        )
        full_name = (
            f"{programme_name} {specialization}"
        ).strip()

        # Exact programme + specialization match
        if full_name and full_name in question:
            matches.append(p)
            continue

        # Programme abbreviation/name match
        if programme_name in words:
            if not specialization or specialization in question:
                matches.append(p)
                continue

        # Specialization match
        if specialization and specialization in words:
            if programme_name in words:
                matches.append(p)
                continue

        # Department match
        if department and department in words:
            if programme_name in words:
                matches.append(p)

    return make_unique(matches)

def make_unique(programmes):
    unique = []
    seen = set()

    for p in programmes:
        key = (
            (p["programme"] or "").strip().lower(),
            (p["specialization"] or "").strip().lower(),
            (p["level"] or "").strip().lower(),
            (p["college"] or "").strip().lower(),
            (p["department"] or "").strip().lower()
        )
        if key not in seen:
            seen.add(key)
            unique.append(p)
    return unique

# new
def normalize_programme_name(text):
    text = normalize_question(text)
    # Remove punctuation/spacing differences in degree names
    text = re.sub(r"\bba\s+bed\b", "ba bed", text)
    text = re.sub(r"\bbsc\s+bed\b", "bsc bed", text)
    return re.sub(r"\s+", " ", text).strip()

def search_programmes(user_question):
    global LAST_PROGRAMME
    question = normalize_question(user_question)
    # all_matches = search_all_matching_programmes(question)
    # if all_matches:
    #     return all_matches[0]

    words = get_words(question)
    programmes = get_all_programmes()
    best_match = None
    best_score = -1

        # --------------------------------------------------
    # DETECT REQUESTED PROGRAMME ONCE FROM THE QUESTION
    # --------------------------------------------------
    requested_programme = None

    if "msc" in words:
        requested_programme = "msc"
    elif "bsc" in words:
        requested_programme = "bsc"
    elif "mca" in words:
        requested_programme = "mca"
    elif "bca" in words:
        requested_programme = "bca"
    elif "mba" in words:
        requested_programme = "mba"
    elif "bba" in words:
        requested_programme = "bba"
    elif "mcom" in words:
        requested_programme = "mcom"
    elif "bcom" in words:
        requested_programme = "bcom"
    elif "med" in words:
        requested_programme = "med"
    elif "bed" in words:
        requested_programme = "bed"
    elif "ma" in words:
        requested_programme = "ma"
    elif "ba" in words:
        requested_programme = "ba"

    print("REQUESTED PROGRAMME:", requested_programme)
    for p in programmes:
        programme_name = normalize_programme_name(
            p["programme"] or ""
        )
        # ) .lower().strip()
        # new
        # normalized_programme = normalize_programme_name(programme_name)

        specialization = normalize_question(
            p["specialization"] or ""
        )
        # ) .lower().strip()

        college = normalize_question(
            p["college"] or ""
        )

        department =  normalize_question(
           p["department"] or ""
        )
        # .lower().strip() 

        # school = (
        #     p["school"] or ""
        # ).lower().strip()

        level = normalize_question (
            p["level"] or ""
        )
        programme_key = programme_name.replace(" ", "")

        if programme_key in ["msc", "m.sc"]:
            programme_key = "msc"
        

        elif programme_key in ["bsc", "b.sc"]:
            programme_key = "bsc"

        elif programme_key in ["ma", "m.a"]:
            programme_key = "ma"

        elif programme_key in ["ba", "b.a"]:
            programme_key = "ba"

        elif programme_key in ["mca", "m.c.a"]:
            programme_key = "mca"

        elif programme_key in ["bca", "b.c.a"]:
            programme_key = "bca"

        elif programme_key in ["mba", "m.b.a"]:
            programme_key = "mba"

        elif programme_key in ["bba", "b.b.a"]:
            programme_key = "bba"

        elif programme_key in ["mcom", "m.com"]:
            programme_key = "mcom"

        elif programme_key in ["bcom", "b.com"]:
            programme_key = "bcom"

        elif programme_key in ["bed", "b.ed"]:
            programme_key = "bed"

        elif programme_key in ["med", "m.ed"]:
            programme_key = "med"
        # .lower().strip()
                # --------------------------------------------------
        # HARD PROGRAMME MATCH
        # --------------------------------------------------
        # If the user explicitly requested MSc/BSc/etc.,
        # do not allow another programme to compete.
        if requested_programme:

            if requested_programme not in get_words(programme_name):
                continue

            # Simple "MSc" means MSc, not Integrated MSc.
            # Integrated MSc is accepted only when the
            # user explicitly says "integrated".
            if (
                requested_programme == "msc"
                and "integrated" in get_words(programme_name)
                and "integrated" not in words
            ):
                continue

            if (
                requested_programme == "bsc"
                and "integrated" in get_words(programme_name)
                and "integrated" not in words
            ):
                continue

        score = 0
        question_key = question.replace(" ", "")
        if programme_key and programme_key in question_key:
            score += 10000
        if programme_name == question:
            score += 10000
        full_name = (
            f"{programme_name} {specialization}"
        ).strip()
        if full_name == question:
            score += 9000
    
        if programme_name:
            programme_words = get_words(programme_name)

            if programme_words.issubset(words):
               score += 5000

        if specialization:
            spec_words = get_words(specialization)

            specialization_matches = (
                spec_words.intersection(words)
            )
            if spec_words.issubset(words):
                score += 4000
            elif specialization_matches:
                score += (
                    len(specialization_matches) * 500
                )

         # Reject programmes with a different specialization
        subject_words = (
            words
            - {
                "what",
                "is",
                "the",
                "fee",
                "fees",
                "of",
                "for",
                "me",
                "tell",
                "about",
                "please",
                "give",
                "information",
                "programme",
                "program",
                "course",
                "intake",
                "seats",
                "duration",
                "eligibility",
                "admission",
                "selection"
            }
            - UG
            - PG
        )

        if subject_words and specialization:
            spec_words = get_words(specialization)

            if not spec_words.intersection(subject_words):
                continue
                # score -= 10000

        if department:
            dept_words = get_words(department)

            if dept_words.issubset(words):
                score += 1000
        if college and college in question:
            score += 1000
        if level == "ug" and words.intersection(UG):
            score += 500

        if level == "pg" and words.intersection(PG):
            score += 500

        if level == "integrated" and "integrated" in words:
            score += 3000
            
        # requested_programme = None
        # if "msc" in words:
        #     requested_programme = "msc"
        # elif "bsc" in words:
        #     requested_programme = "bsc"
        # elif "mca" in words:
        #     requested_programme = "mca"
        # elif "bca" in words:
        #     requested_programme = "bca"
        # elif "mba" in words:
        #     requested_programme = "mba"

        # elif "bba" in words:
        #     requested_programme = "bba"

        # elif "mcom" in words:
        #     requested_programme = "mcom"

        # elif "bcom" in words:
        #     requested_programme = "bcom"

        # elif "med" in words:
        #     requested_programme = "med"

        # elif "bed" in words:
        #     requested_programme = "bed"

        # elif "ma" in words:
        #     requested_programme = "ma"

        # elif "ba" in words:
        #     requested_programme = "ba"
    #     if requested_programme:
    #         if programme_name == requested_programme:
    #             score += 5000
    #         elif (
    #              level == "integrated"
    #              and "integrated" in words
    #              and requested_programme in get_words(
    #              programme_name.replace("integrated", "").strip()
    #             )
    #         ):
    #             score += 5000

    # # Different programme
    #         elif requested_programme not in get_words(
    #             programme_name
    #         ):
    #             score -= 3000
        if score > best_score:
            best_score = score
            best_match = p
        

    if best_match and best_score > 0:
        LAST_PROGRAMME = best_match
        print(
            "BEST PROGRAMME:",
            best_match["programme"],
            "|",
            best_match["specialization"],
            "|",
            best_match["level"],
            "|",
            best_match["college"],
            "| SCORE:",
            best_score
        )
        return best_match
    return None
            

        # new 3
        # if normalized_programme in question:
        #  score += 3000
        # if (
        #    "integrated" in words
        #    and "ba" in words
        #    and "bed" in words
        # ):
        #     if (
        #         level == "integrated"
        #         and "ba" in normalized_programme
        #         and "bed" in normalized_programme
        #     ):
        #         score += 5000
        #     else:
        #         score -= 1000
        # if (
        #     "integrated" in words
        #     and "bsc" in words
        #     and "bed" in words
        # ):
        #     if (
        #         level == "integrated"
        #         and "bsc" in normalized_programme
        #         and "bed" in normalized_programme
        #     ):
        #         score += 5000
        #     else:
        #         score -= 1000
        # if normalized_programme == question:
        #     score += 10000
        # elif normalized_programme in question:
        #     score += 3000
        # elif programme_name in words:
        #     score += 1000

        # if specialization:
        #     spec_words = get_words(specialization)
        #     score += len(
        #         spec_words.intersection(words)
        #     ) * 50

        # if department:
        #     dept_words = get_words(department)
        #     score += len(
        #         dept_words.intersection(words)
        #     ) * 20

        # if college and college in question:
        #     score += 50

        # if school and school in question:
        #     score += 20

        # if level == "pg" and words.intersection(PG):
        #     score += 80

        # if level == "ug" and words.intersection(UG):
        #     score += 80

        # if "integrated" in words:
        #     if level == "integrated":
        #         score += 100
        #     else:
        #         score -= 100

        # if score > best_score:
        #     best_score = score
        #     best_match = p

    # if best_match:
    #     LAST_PROGRAMME = best_match
    # return best_match

    # new added ib
    # if best_match and best_score > 0:
    #     LAST_PROGRAMME = best_match
    #     return best_match
    # return None

def search_all_matching_programmes(user_question):
    question = normalize_question(user_question)
    words = get_words(question)
    programmes = get_all_programmes()

    matches = []

    # ---------------------------------------------------------
    # DETERMINE REQUESTED PROGRAMME
    # ---------------------------------------------------------

    requested_programme = None

    programme_order = [
        "msc",
        "bsc",
        "mca",
        "bca",
        "mba",
        "bba",
        "mcom",
        "bcom",
        "med",
        "bed",
        "ma",
        "ba"
    ]

    for programme in programme_order:
        if programme in words:
            requested_programme = programme
            break

    # ---------------------------------------------------------
    # DETERMINE WHETHER INTEGRATED WAS REQUESTED
    # ---------------------------------------------------------

    requested_integrated = (
        "integrated" in words
    )

    print(
        "REQUESTED PROGRAMME:",
        requested_programme
    )

    print(
        "REQUESTED INTEGRATED:",
        requested_integrated
    )

    # ---------------------------------------------------------
    # DETERMINE SUBJECT WORDS ONCE
    # ---------------------------------------------------------

    ignored_words = {
        "which",
        "what",
        "college",
        "colleges",
        "offer",
        "offers",
        "offering",
        "provide",
        "provides",
        "provided",
        "programme",
        "programmes",
        "program",
        "programs",
        "course",
        "courses",
        "the",
        "a",
        "an",
        "of",
        "in",
        "for",
        "where",
        "can",
        "i",
        "study",
        "to",
        "me",
        "is",
        "are",
        "available",
        "show",
        "list",
        "all",
        "have",
        "has",
        "please",
        "tell",
        "give",
        "information",
        "about",
        "fee",
        "fees",
        "intake",
        "duration",
        "eligibility",
        "admission",
        "selection",
        "process"
    }

    requested_subject_words = (
        words - ignored_words - UG - PG
    )

    requested_subject_words.discard(
        "integrated"
    )

    print(
        "REQUESTED SUBJECT WORDS:",
        requested_subject_words
    )

    # ---------------------------------------------------------
    # CHECK EVERY PROGRAMME
    # ---------------------------------------------------------

    for p in programmes:

        programme_name = (
            p["programme"] or ""
        ).lower().strip()

        specialization = (
            p["specialization"] or ""
        ).lower().strip()

        department = (
            p["department"] or ""
        ).lower().strip()

        level = (
            p["level"] or ""
        ).lower().strip()

        normalized_programme = (
            normalize_programme_name(
                programme_name
            )
        )

        programme_words = get_words(
            normalized_programme
        )

        # -----------------------------------------------------
        # PROGRAMME MATCH
        # -----------------------------------------------------

        if requested_programme:

            if requested_programme not in programme_words:
                continue

        # -----------------------------------------------------
        # INTEGRATED / NON-INTEGRATED MATCH
        # -----------------------------------------------------

        if requested_integrated:

            # User explicitly asked for Integrated.
            # Therefore only Integrated programmes are allowed.
            if level != "integrated":
                continue

        else:

            # User did NOT ask for Integrated.
            # Therefore do not return Integrated versions.
            if level == "integrated":
                continue

        # -----------------------------------------------------
        # SUBJECT MATCH
        # -----------------------------------------------------

        searchable_words = (
            get_words(programme_name)
            | get_words(specialization)
            | get_words(department)
        )

        if requested_subject_words:

            subject_matches = (
                requested_subject_words.intersection(
                    searchable_words
                )
            )

            if not subject_matches:
                continue

        # -----------------------------------------------------
        # SCORING
        # -----------------------------------------------------

        score = 0

        # Exact programme match
        if requested_programme:

            if programme_name == requested_programme:
                score += 10000

            elif (
                requested_programme
                in programme_words
            ):
                score += 8000

        # Integrated exactness
        if requested_integrated:

            if level == "integrated":
                score += 5000

        # Subject / specialization match
        specialization_words = get_words(
            specialization
        )

        specialization_matches = (
            specialization_words.intersection(
                requested_subject_words
            )
        )

        if specialization_matches:

            if specialization_words.issubset(
                requested_subject_words
            ):
                score += 4000

            else:
                score += (
                    len(specialization_matches) * 1000
                )

        # Department match
        department_words = get_words(
            department
        )

        department_matches = (
            department_words.intersection(
                requested_subject_words
            )
        )

        if department_matches:
            score += (
                len(department_matches) * 100
            )

        # Exact normalized programme in question
        if normalized_programme in question:
            score += 3000

        matches.append(
            (score, p)
        )

    # ---------------------------------------------------------
    # NO MATCHES
    # ---------------------------------------------------------

    if not matches:
        return []

    # ---------------------------------------------------------
    # FIND HIGHEST SCORE
    # ---------------------------------------------------------

    best_score = max(
        score
        for score, _ in matches
    )

    results = [
        p
        for score, p in matches
        if score == best_score
    ]

    return make_unique(results)

# def search_all_matching_programmes(user_question):
#     question = normalize_question(user_question)
#     words = get_words(question)
#     programmes = get_all_programmes()
#     matches = []
#     requested_programme = None

#     if "msc" in words:
#         requested_programme = "msc"

#     elif "bsc" in words:
#         requested_programme = "bsc"

#     elif "mca" in words:
#         requested_programme = "mca"

#     elif "bca" in words:
#         requested_programme = "bca"

#     elif "mba" in words:
#         requested_programme = "mba"

#     elif "bba" in words:
#         requested_programme = "bba"

#     elif "mcom" in words:
#         requested_programme = "mcom"

#     elif "bcom" in words:
#         requested_programme = "bcom"

#     elif "med" in words:
#         requested_programme = "med"

#     elif "bed" in words:
#         requested_programme = "bed"

#     elif "ma" in words:
#         requested_programme = "ma"

#     elif "ba" in words:
#         requested_programme = "ba"

#     print(
#         "REQUESTED PROGRAMME:",
#         requested_programme
#     )
#     for p in programmes:
#         programme_name = (
#             p["programme"] or ""
#         ).lower().strip()

#         specialization = (
#             p["specialization"] or ""
#         ).lower().strip()

#         department = (
#             p["department"] or ""
#         ).lower().strip()

#         level = (
#             p["level"] or ""
#         ).lower().strip()

#         # if requested_programme:

#         normalized_programme = normalize_programme_name(
#             programme_name
#         )

#         # Remove "integrated" only for checking whether
#         # the programme itself is MSc/BSc/etc.
#         programme_words = get_words(
#             normalized_programme
#         )

#         # Example:
#         # "msc" -> {"msc"}
#         # "integrated msc" -> {"integrated", "msc"}
#         # "bsc" -> {"bsc"}

#         if requested_programme not in programme_words:
#             continue

#         # IMPORTANT:
#         # If user asked for MSc, do NOT include
#         # Integrated MSc.
#         if (
#             requested_programme == "msc"
#             and "integrated" in programme_words
#         ):
#             continue

#         if (
#             requested_programme == "bsc"
#             and "integrated" in programme_words
#         ):
#             continue

#         if (
#             requested_programme == "ma"
#             and "integrated" in programme_words
#         ):
#             continue

#         if (
#             requested_programme == "ba"
#             and "integrated" in programme_words
#         ):
#             continue

#         if (
#             requested_programme == "mca"
#             and "integrated" in programme_words
#         ):
#             continue

#         if (
#             requested_programme == "mba"
#             and "integrated" in programme_words
#         ):
#             continue

#         if (
#             requested_programme == "bba"
#             and "integrated" in programme_words
#         ):
#             continue

#         if (
#             requested_programme == "bca"
#             and "integrated" in programme_words
#         ):
#             continue

#         # normalized_programme = (
#         #     normalize_programme_name(programme_name)
#         # )

#         score = 0

#         if normalized_programme in question:
#             score += 3000

#         specialization_words = get_words(
#             specialization
#         )
#         specialization_matches = (
#             specialization_words.intersection(words)
#         )
#         if specialization_matches:
#             score += (
#                 len(specialization_matches) * 500
#             )
#         department_words = get_words(
#             department
#         )
#         department_matches = (
#             department_words.intersection(words)
#         )
#         if department_matches:
#             score += (
#                 len(department_matches) * 100
#             )

#         # if "msc" in words:
#         #    if programme_name == "msc" and level == "pg":
#         #       score += 5000
#         #    elif level != "pg":
#         #       score -= 5000

#         # elif "bsc" in words:
#         #    if programme_name == "bsc" and level == "ug":
#         #       score += 5000
#         #    elif level != "ug":
#         #       score -= 5000

#         # elif "ma" in words:
#         #    if programme_name == "ma" and level == "pg":
#         #       score += 5000
#         #    elif level != "pg":
#         #       score -= 5000

#         # elif "ba" in words:
#         #    if programme_name == "ba" and level == "ug":
#         #       score += 5000
#         #    elif level != "ug":
#         #       score -= 5000

#         # elif "mca" in words:
#         #    if programme_name == "mca" and level == "pg":
#         #       score += 5000
#         #    elif level != "pg":
#         #       score -= 5000

#         # elif "bca" in words:
#         #    if programme_name == "bca" and level == "ug":
#         #       score += 5000
#         #    elif level != "ug":
#         #       score -= 5000

#         # elif "mba" in words:
#         #    if programme_name == "mba" and level == "pg":
#         #       score += 5000
#         #    elif level != "pg":
#         #       score -= 5000

#         # elif "bba" in words:
#         #    if programme_name == "bba" and level == "ug":
#         #       score += 5000
#         #    elif level != "ug":
#         #       score -= 5000

#         # elif "mcom" in words:
#         #    if programme_name == "mcom" and level == "pg":
#         #       score += 5000
#         #    elif level != "pg":
#         #       score -= 5000

#         # elif "bcom" in words:
#         #    if programme_name == "bcom" and level == "ug":
#         #       score += 5000
#         #    elif level != "ug":
#         #       score -= 5000
#         # elif "bed" in words:
#         #    if programme_name == "bed" and level == "ug":
#         #       score += 5000
#         #    elif level != "ug":
#         #       score -= 5000

#         # elif "med" in words:
#         #    if programme_name == "med" and level == "pg":
#         #       score += 5000
#         #    elif level != "pg":
#         #       score -= 5000
#         if "integrated" in words:

#            if level == "integrated":
#               score += 5000
#            else:
#               score -= 5000
        
#         # if level == "pg" and words.intersection(PG):
#         #     score += 80
#         # if level == "ug" and words.intersection(UG):
#         #     score += 80

#         # if "integrated" in words:

#         #     if level == "integrated":
#         #         score += 100

#         #     else:
#         #         score -= 100
#         requested_subject_words = (
#             words
#             - {
#                 "which",
#                 "what",
#                 "college",
#                 "colleges",
#                 "offer",
#                 "offers",
#                 "offering",
#                 "provide",
#                 "provides",
#                 "provided",
#                 "programme",
#                 "programmes",
#                 "program",
#                 "programs",
#                 "course",
#                 "courses",
#                 "the",
#                 "a",
#                 "an",
#                 "of",
#                 "in",
#                 "for",
#                 "where",
#                 "can",
#                 "i",
#                 "study",
#                 "to",
#                 "me",
#                 "is",
#                 "are",
#                 "available",
#                 "show",
#                 "list",
#                 "all",
#                 "have",
#                 "has"
#             }
#         )
#         requested_subject_words -= (
#             UG | PG
#         )
#         requested_subject_words.discard(
#             "integrated"
#         )
#         if requested_subject_words:

#             searchable_words = (
#                 get_words(programme_name)
#                 | get_words(specialization)
#                 | get_words(department)
#             )

#             subject_matches = (
#                 requested_subject_words.intersection(
#                     searchable_words
#                 )
#             )

#             if not subject_matches:
#                 continue
#         matches.append((score,p))

#     if not matches:
#         return []

#     if requested_subject_words:
#        subject_results = []
#        for score, p in matches:
#           programme_name = (
#            p["programme"] or ""
#           ).lower().strip()

#           specialization = (
#             p["specialization"] or ""
#           ).lower().strip()

#           department = (
#             p["department"] or ""
#           ).lower().strip()

#           searchable_words = (
#             get_words(programme_name)
#             | get_words(specialization)
#             | get_words(department)
#           )

#           subject_matches = (
#             requested_subject_words.intersection(
#                 searchable_words
#             )
#           )

#           if subject_matches:
#              subject_results.append(p)

#        if subject_results:
#              return make_unique(subject_results)

#     best_score = max(
#         score 
#         for score, _ in matches
#     )
#     results = [
#         p for score, p in matches
#         if score == best_score
#     ]
#     return make_unique(results)

def search_programme_list(question):

    question = normalize_question(question)
    question = re.sub(
        r"\bm\s+sc\b",
        "msc",
        question
    )

    question = re.sub(
        r"\bb\s+sc\b",
        "bsc",
        question
    )

    question = re.sub(
        r"\bm\s+com\b",
        "mcom",
        question
    )

    question = re.sub(
        r"\bb\s+com\b",
        "bcom",
        question
    )

    question = re.sub(
        r"\bm\s+ca\b",
        "mca",
        question
    )

    question = re.sub(
        r"\bb\s+ca\b",
        "bca",
        question
    )

    question = re.sub(
        r"\bm\s+ba\b",
        "mba",
        question
    )

    question = re.sub(
        r"\bb\s+ba\b",
        "bba",
        question
    )

    question = re.sub(
        r"\bm\s+a\b",
        "ma",
        question
    )

    question = re.sub(
        r"\bb\s+a\b",
        "ba",
        question
    )

    question = re.sub(
        r"\bm\s+ed\b",
        "med",
        question
    )

    question = re.sub(
        r"\bb\s+ed\b",
        "bed",
        question
    )
    typo_replacements = {
        "programmemes": "programmes",
        "programmee": "programme",
        "programm": "programme",
        "programs": "programmes"
    }
    for old, new in typo_replacements.items():
        question = re.sub( rf"\b{re.escape(old)}\b", new,question)

    print("------------------------------------------------")
    print("LIST SEARCH QUESTION:", question)

    requested_level = None

    if re.search(r"\bintegrated\b", question):
        requested_level = "integrated"

    elif re.search(
        r"\b(pg|postgraduate|post graduate)\b",
        question
    ):
        requested_level = "pg"

    elif re.search(
        r"\b(ug|undergraduate|under graduate)\b",
        question
    ):
        requested_level = "ug"

    print("REQUESTED LEVEL:", requested_level)

    ignore_words = {
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
        "programmemes",
        "program",
        "programs",
        "course",
        "courses",
        "all",
        "can",
        "study",
        "where",
        "to",
        "in",
        "for",
        "the",
        "of",
        "are",
        "is",
        "what",
        "does",
        "do",
        "me",
        "i",
        "my",
        "pg",
        "ug",
        "postgraduate",
        "post",
        "graduate",
        "undergraduate",
        "under",
        "integrated"
    }

    keywords = [
        word
        for word in re.findall(
            r"[a-z0-9]+(?:-[a-z0-9]+)*",
            question
        )
        if word not in ignore_words
    ]

    keywords = list(dict.fromkeys(keywords))

    print("LIST KEYWORDS:", keywords)

    programmes = get_all_programmes()

    results = []

    for p in programmes:

        level = (
            p["level"] or ""
        ).lower().strip()

        if requested_level and level != requested_level:
            continue

        programme_name = (
            p["programme"] or ""
        ).lower().strip()

        specialization = (
            p["specialization"] or ""
        ).lower().strip()

        department = (
            p["department"] or ""
        ).lower().strip()

        college = (
            p["college"] or ""
        ).lower().strip()

        school = (
            p["school"] or ""
        ).lower().strip()

        programme_words = get_words(programme_name)
        specialization_words = get_words(specialization)
        department_words = get_words(department)
        college_words = get_words(college)
        school_words = get_words(school)

        search_words = (
            programme_words
            | specialization_words
            | department_words
            | college_words
            | school_words
        )

        if not keywords:
            results.append(p)
            continue

        matched = True

        for keyword in keywords:

            if keyword == "information":
                if (
                    "information" not in programme_name
                    and "information" not in specialization
                    and "information" not in department
                ):
                    matched = False
                    break

            elif keyword == "technology":
                if (
                    "technology" not in programme_name
                    and "technology" not in specialization
                    and "technology" not in department
                ):
                    matched = False
                    break

            elif keyword not in search_words:
                matched = False
                break

        if matched:
            results.append(p)

    results = make_unique(results)

    level_order = {
        "ug": 1,
        "integrated": 2,
        "pg": 3
    }

    results.sort(
        key=lambda x: (
            level_order.get(
                (x["level"] or "").lower(),
                99
            ),
            (x["programme"] or "").lower(),
            (x["specialization"] or "").lower(),
            (x["college"] or "").lower()
        )
    )

    print("FINAL RESULTS:", len(results))

    for p in results:
        print(
            "RESULT:",
            p["programme"],
            "|",
            p["specialization"],
            "|",
            p["level"],
            "|",
            p["college"]
        )

    return results


def get_last_programme():
    return LAST_PROGRAMME