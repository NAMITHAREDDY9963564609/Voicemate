from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import json
import uuid
import requests
from tts_clone import generate_reply
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "your_secret_key"

USERS_FILE = "users.json"
UPLOAD_FOLDER = "static/audio"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Ensure users.json exists
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump([], f)

def load_users():
    with open(USERS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        users = load_users()

        for user in users:
            if user.get("username") == username and user.get("password") == password:
                session["user"] = username
                return redirect(url_for("welcome"))
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        users = load_users()

        if any(user.get("username") == username for user in users):
            return render_template("signup.html", error="Username already exists")

        users.append({"email": email, "username": username, "password": password})
        save_users(users)
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        session["bot_name"] = request.form.get("bot_name")
        return redirect(url_for("upload_voice"))

    return render_template("welcome.html", username=session["user"])

@app.route("/upload_voice", methods=["GET", "POST"])
def upload_voice():
    if "user" not in session or "bot_name" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        voice_file = request.files.get("voice")
        if not voice_file:
            return render_template("upload_voice.html", error="Please upload your voice.")

        voice_path = os.path.join(UPLOAD_FOLDER, f"{session['user']}_voice.wav")
        voice_file.save(voice_path)
        session["voice_path"] = voice_path
        return redirect(url_for("chat"))

    return render_template("upload_voice.html")

@app.route("/chat")
def chat():
    if "user" not in session or "voice_path" not in session:
        return redirect(url_for("login"))
    return render_template("chat.html", bot_name=session.get("bot_name", "VoiceMate"))

@app.route("/get_response", methods=["POST"])
def get_response():
    if "voice_path" not in session:
        return jsonify({"error": "Voice not uploaded"}), 400

    data = request.get_json()
    user_message = data.get("message")

    # Get AI reply using OpenRouter
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": user_message}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    try:
        ai_text = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("AI error:", e)
        return jsonify({"error": "AI response failed"}), 500

    print("🧠 AI says:", ai_text)

    # Generate voice reply
    uid = str(uuid.uuid4())[:8]
    reply_path = os.path.join(UPLOAD_FOLDER, f"reply_{uid}.wav")
    try:
        generate_reply(ai_text, session["voice_path"], reply_path)
    except Exception as e:
        print("Voice error:", e)
        return jsonify({"error": "Voice generation failed"}), 500

    return jsonify({"audio_path": "/" + reply_path})

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
