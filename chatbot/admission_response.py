# import re
# from chatbot.admission_search import search_admission

# def clean_question(question):
#     question = question.lower().strip()
#     question = re.sub(
#         r"\s+",
#         " ",
#         question
#     )
#     return question

# def admission_response(question):
#     print("Admission Module Called")
#     print(
#         "ADMISSION RESPONSE QUESTION:",
#         repr(question)
#     )

#     question = clean_question(question)

#     result = search_admission(question)

#     if result is None:
#         return (
#             "I'm sorry, I couldn't find matching "
#             "admission information. Please check the "
#             "question or try another admission-related query."
#         )

#     # -------------------------------------------------
#     # REQUIRED DOCUMENTS
#     # -------------------------------------------------

#     if any(
#         phrase in question
#         for phrase in [
#             "required document",
#             "required documents",
#             "documents required",
#             "documents needed",
#             "documents do i need",
#             "what documents",
#             "which documents",
#             "document required"
#         ]
#     ):
#         return (
#             f"🎓 <b>{result['topic']}</b>\n\n"
#             f"<b>Required Documents:</b>\n"
#             f"{result['required_documents']}"
#         )

#     # -------------------------------------------------
#     # ELIGIBILITY
#     # -------------------------------------------------

#     if any(
#         phrase in question
#         for phrase in [
#             "eligibility",
#             "eligible",
#             "who can apply",
#             "who is eligible",
#             "qualification",
#             "qualifications",
#             "eligibility criteria"
#         ]
#     ):
#         return (
#             f"🎓 <b>{result['topic']}</b>\n\n"
#             f"<b>Eligibility:</b>\n"
#             f"{result['eligibility_basis']}"
#         )

#     # -------------------------------------------------
#     # APPLICATION FEE
#     # -------------------------------------------------

#     if any(
#         phrase in question
#         for phrase in [
#             "application fee",
#             "application fees",
#             "admission fee",
#             "registration fee",
#             "how much is the fee",
#             "how much fee",
#             "fee for admission"
#         ]
#     ):
#         return (
#             f"💰 <b>{result['topic']}</b>\n\n"
#             f"<b>Application Fee:</b>\n"
#             f"{result['application_fee']}"
#         )

#     # -------------------------------------------------
#     # ADMISSION MODE
#     # -------------------------------------------------

#     if any(
#         phrase in question
#         for phrase in [
#             "how to apply",
#             "how do i apply",
#             "where to apply",
#             "how can i apply",
#             "application mode",
#             "admission mode",
#             "apply online",
#             "apply for admission"
#         ]
#     ):
#         return (
#             f"🎓 <b>{result['topic']}</b>\n\n"
#             f"<b>Admission Mode:</b>\n"
#             f"{result['admission_mode']}\n\n"
#             f"<b>Admission Portal:</b>\n"
#             f"{result['admission_portal']}"
#         )

#     # -------------------------------------------------
#     # SELECTION
#     # -------------------------------------------------

#     if any(
#         phrase in question
#         for phrase in [
#             "selection",
#             "how are students selected",
#             "selection process",
#             "selection basis",
#             "how selection is done",
#             "merit"
#         ]
#     ):
#         return (
#             f"🎓 <b>{result['topic']}</b>\n\n"
#             f"<b>Selection Basis:</b>\n"
#             f"{result['selection_basis']}"
#         )

#     # -------------------------------------------------
#     # RESERVATION
#     # -------------------------------------------------

#     if any(
#         phrase in question
#         for phrase in [
#             "reservation",
#             "reserved category",
#             "reservation policy",
#             "reserved seats",
#             "category reservation"
#         ]
#     ):
#         return (
#             f"🎓 <b>{result['topic']}</b>\n\n"
#             f"<b>Reservation:</b>\n"
#             f"{result['reservation']}"
#         )

#     # -------------------------------------------------
#     # ADMISSION PORTAL
#     # -------------------------------------------------

#     if any(
#         phrase in question
#         for phrase in [
#             "admission portal",
#             "admission website",
#             "where can i apply",
#             "official admission website",
#             "admission link"
#         ]
#     ):
#         return (
#             f"🌐 <b>{result['topic']}</b>\n\n"
#             f"<b>Admission Portal:</b>\n"
#             f"{result['admission_portal']}\n\n"
#             f"<b>Official Link:</b>\n"
#             f"{result['url']}"
#         )

#     # -------------------------------------------------
#     # GENERAL ADMISSION INFORMATION
#     # -------------------------------------------------

#     return (
#         f"🎓 <b>{result['topic']}</b>\n\n"
#         f"{result['description']}\n\n"
#         f"<b>Applicable To:</b>\n"
#         f"{result['applicable_to']}\n\n"
#         f"<b>Eligibility:</b>\n"
#         f"{result['eligibility_basis']}\n\n"
#         f"<b>Admission Mode:</b>\n"
#         f"{result['admission_mode']}\n\n"
#         f"<b>Selection:</b>\n"
#         f"{result['selection_basis']}\n\n"
#         f"<b>Important Notes:</b>\n"
#         f"{result['important_notes']}"
#     )