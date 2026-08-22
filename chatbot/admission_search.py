
# import sqlite3
# import re

# DATABASE_NAME = "chatbot/knowledge.db"


# def get_connection():
#     return sqlite3.connect(DATABASE_NAME)


# def clean_question(question):
#     question = question.lower().strip()
#     question = re.sub(r"[?.,!]", " ", question)
#     question = re.sub(r"\s+", " ", question)
#     return question


# def search_admission(question):

#     question = clean_question(question)

#     print("ADMISSION SEARCH:", question)

#     # -------------------------------------------------
#     # DETECT PROGRAMME LEVEL
#     # -------------------------------------------------

#     programme_level = None

#     if re.search(r"\bug\b|\bundergraduate\b|\bfyug\b|\bbachelor\b", question):
#         programme_level = "ug"

#     elif re.search(r"\bpg\b|\bpostgraduate\b|\bpost graduate\b|\bmaster\b|\bmasters\b", question):
#         programme_level = "pg"

#     elif "integrated" in question:
#         programme_level = "integrated"

#     print("DETECTED PROGRAMME LEVEL:", programme_level)

#     # -------------------------------------------------
#     # DETECT ADMISSION TOPIC
#     # -------------------------------------------------

#     topic_phrases = {

#         "required documents": [
#             "required documents",
#             "required document",
#             "documents required",
#             "documents needed",
#             "what documents",
#             "which documents",
#             "documents do i need"
#         ],

#         "eligibility": [
#             "eligibility",
#             "eligible",
#             "who can apply",
#             "who is eligible",
#             "qualification",
#             "qualifications"
#         ],

#         "fee payment": [
#             "application fee",
#             "application fees",
#             "admission fee",
#             "registration fee",
#             "fee for admission",
#             "how much is the fee",
#             "how much fee"
#         ],

#         "application process": [
#             "how can i apply",
#             "how do i apply",
#             "how to apply",
#             "where to apply",
#             "apply online",
#             "apply for admission",
#             "application process",
#             "admission process"
#         ],

#         "selection basis": [
#             "how are students selected",
#             "how students are selected",
#             "selection process",
#             "selection basis",
#             "how selection is done",
#             "how is admission decided",
#             "selection",
#             "merit"
#         ],

#         "reservation policy": [
#             "reservation policy",
#             "reservation",
#             "reserved category",
#             "reserved seats"
#         ],

#         "admission portal": [
#             "admission portal",
#             "admission website",
#             "admission link",
#             "official admission website"
#         ],

#         "migration certificate": [
#             "migration certificate",
#             "migration"
#         ],

#         "spot admission": [
#             "spot admission",
#             "spot admissions"
#         ],

#         "admission deadline": [
#             "admission deadline",
#             "application deadline",
#             "last date for admission",
#             "last date to apply",
#             "last date",
#             "deadline"
#         ],

#         "counselling": [
#             "counselling",
#             "counseling",
#             "counselling process",
#             "counseling process"
#         ]
#     }

#     detected_topic = None
#     best_phrase_length = 0

#     for topic, phrases in topic_phrases.items():

#         for phrase in phrases:

#             if phrase in question:

#                 # Prefer the longest matching phrase
#                 length = len(phrase.split())

#                 if length > best_phrase_length:
#                     detected_topic = topic
#                     best_phrase_length = length

#     print("DETECTED ADMISSION TOPIC:", detected_topic)

#     # -------------------------------------------------
#     # GET ADMISSION RECORDS
#     # -------------------------------------------------

#     conn = get_connection()
#     conn.row_factory = sqlite3.Row
#     cursor = conn.cursor()

#     cursor.execute("SELECT * FROM admissions")
#     results = cursor.fetchall()

#     conn.close()

#     if not results:
#         return None

#     # -------------------------------------------------
#     # SCORE RECORDS
#     # -------------------------------------------------

#     best_result = None
#     best_score = -1

#     for result in results:

#         topic = str(result["topic"] or "").lower()
#         record_level = str(result["programme_level"] or "").lower()

#         score = 0

#         # -------------------------------------------------
#         # TOPIC MATCH
#         # -------------------------------------------------

#         if detected_topic:

#             if detected_topic in topic:
#                 score += 100

#         # -------------------------------------------------
#         # PROGRAMME LEVEL
#         # Only used as a secondary match
#         # -------------------------------------------------

#         if programme_level:

#             if programme_level == "ug":

#                 if any(x in record_level for x in [
#                     "ug",
#                     "undergraduate",
#                     "fyug"
#                 ]):
#                     score += 30

#                 elif "pg" in record_level:
#                     score -= 30

#             elif programme_level == "pg":

#                 if any(x in record_level for x in [
#                     "pg",
#                     "postgraduate",
#                     "post graduate"
#                 ]):
#                     score += 30

#                 elif "ug" in record_level:
#                     score -= 30

#             elif programme_level == "integrated":

#                 if "integrated" in record_level:
#                     score += 30

#         # General records apply to everyone
#         if "all programmes" in record_level:
#             score += 10

#         print(
#             f"TOPIC: {result['topic']} | SCORE: {score}"
#         )

#         if score > best_score:
#             best_score = score
#             best_result = result

#     # -------------------------------------------------
#     # RETURN BEST RESULT
#     # -------------------------------------------------

#     if best_result:

#         print(
#             "BEST ADMISSION RESULT:",
#             best_result["topic"],
#             "| SCORE:",
#             best_score
#         )

#         print(
#             "TOPIC:",
#             best_result["topic"]
#         )

#         print(
#             "APPLICABLE TO:",
#             best_result["applicable_to"]
#         )

#     return best_result

