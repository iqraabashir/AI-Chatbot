import os
from flask import Flask, jsonify, render_template, request,send_from_directory 
from chatbot.intents import get_response
from chatbot.cus_website_data import (
    create_cus_website_table,
    fetch_notifications,
    fetch_results
)
from chatbot.translation import (
    translate_to_english,
    translate_from_english
)
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
from admin import admin
app.register_blueprint(admin)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def chatbot_response():
    print("========== TRANSLATION ROUTE ==========")
    data = request.get_json()
    print(f"Request data: {data}")
    user_message = data["message"]
    language = data.get("language", "en")
    try:
        english_message = translate_to_english(
            user_message,
            language
          )

        print("========== BEFORE CHATBOT ==========")
        print("Original question:", user_message) 
        print("English question:", english_message)

        bot_reply = get_response(english_message)
        translated_reply = translate_from_english(
           bot_reply,
           language
          )

    except Exception as e:
        print("Translation error:", e)
    
        translated_reply = (
            "Sorry, I’m unable to process " "your request in this language right now. " 
            "Please try again or use English."
           )
    print(f"Bot reply: {translated_reply}")
    return jsonify({
       "response": translated_reply
    })
 
@app.route("/prospectus")
def prospectus():
    pdf_directory = os.path.join(
        app.root_path,
        "data",
        "official_data",
        "pdfs"
    )

    return send_from_directory(
        pdf_directory,
        "Prospectus.pdf"
    )


if __name__ == "__main__":
    print("Updating CUS website data...")
    try:
        create_cus_website_table()
        notification_count = fetch_notifications()
        result_count = fetch_results()
        print(
            f"CUS website data updated successfully. "
            f"Notifications: {notification_count}, "
            f"Results: {result_count}"
        )
    except Exception as e:
        print("CUS website update failed:", e)
    app.run(debug=True)