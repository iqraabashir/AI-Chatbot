from chatbot.nlp import preprocess_text
from chatbot.database import search_question
from chatbot.response_builder import build_response

def get_response(message):
    return build_response(message)

# def get_response(message):
#      db_response = search_question(message)

#      if db_response:
#         return db_response
     
#      words = preprocess_text(message)
#      if "hi" in words or "hello" in words:
#         return "Hello! How can I help you today?"

#      elif "admiss" in words:
#         return "Admissions are open. Please visit the admission section."

#      elif "fee" in words:
#          return "Please check the fee structure on the official website."

#      elif "exam" in words:
#         return "Exam schedules are published in the notice section."

#      elif "cours" in words:
#         return "We offer MCA, MSc IT, BCA and other programs."

#      elif "library" in words:
#         return "The library is open from 9 AM to 5 PM."

#      else:
#         return "Sorry, I do not understand your question."
