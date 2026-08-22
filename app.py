import os
from flask import Flask, jsonify, render_template, request,send_from_directory 
from chatbot.intents import get_response
from chatbot.cus_website_data import (
    create_cus_website_table,
    fetch_notifications,
    fetch_results
)

app = Flask(__name__)
app.secret_key = "cluster_university_secret_key"
from admin import admin
app.register_blueprint(admin)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def chatbot_response():
    print("Received request for chatbot response")
    data = request.get_json()
    print(f"Request data: {data}")
    user_message = data["message"]
    bot_reply = get_response(user_message)
    print(f"Bot reply: {bot_reply}")
    return jsonify({
        "response": bot_reply
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