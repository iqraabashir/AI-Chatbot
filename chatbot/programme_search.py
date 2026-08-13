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
        # .lower().strip()

        score = 0
        if programme_name == question:
            score += 10000
        full_name = (
            f"{programme_name} {specialization}"
        ).strip()
        if full_name == question:
            score += 9000

        if programme_name and programme_name in words:
            score += 5000

        if specialization:
            spec_words = get_words(specialization)

            if spec_words.issubset(words):
                score += 4000
            else:
                score += (
                    len(spec_words.intersection(words)) * 500
                )

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
            score += 500
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
            normalize_programme_name(programme_name)
        )

        score = 0

        if normalized_programme in question:
            score += 3000

        if specialization:
            spec_words = get_words(specialization)
            score += len(
                spec_words.intersection(words)
            ) * 50

        if department:
            dept_words = get_words(department)
            score += len(
                dept_words.intersection(words)
            ) * 20

        if level == "pg" and words.intersection(PG):
            score += 80

        if level == "ug" and words.intersection(UG):
            score += 80

        if "integrated" in words:
            if level == "integrated":
                score += 100
            else:
                score -= 100

        if score > 0:
            matches.append((score, p))

    if not matches:
        return []

    best_score = max(
        score for score, p in matches
    )

    results = [
        p for score, p in matches
        if score == best_score
    ]

    return make_unique(results)
def search_programme_list(question):

    question = normalize_question(question)
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