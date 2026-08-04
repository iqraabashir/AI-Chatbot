from flask import Flask, jsonify, render_template, request
from chatbot.intents import get_response



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
    

if __name__ == "__main__":
    app.run(debug=True)