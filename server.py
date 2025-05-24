from flask import Flask, request, jsonify, render_template, redirect, session
import json
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

DB_FILE = "db/users.json"
MESSAGES_FILE = "db/messages.json"

def load_users():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, 'r') as f:
        return json.load(f)
    
def save_users(users):
    with open(DB_FILE, 'w') as f:
        json.dump(users, f)

def load_messanges():
    if not os.path.exists(MESSAGES_FILE):
        return []
    with open(MESSAGES_FILE, 'r') as f:
        return json.load(f)
    
def save_messages(messages):
    with open(MESSAGES_FILE, 'w') as f:
        json.dump(messages, f)

@app.route('/')
def home():
    return redirect('/register')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    users = load_users()
    username = data['username']
    password = data['password']

    if username in users and users[username] == password:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "Неверный логин или пароль"})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    users = load_users()
    username = data['username']
    password = data['password']

    if username in users:
        return jsonify({"success": False, "message": "Пользователь уже существует"})
    users[username] = password
    save_users(users)
    return jsonify({"success": True})

@app.route('/messages', methods=['GET'])
def get_messages():
    return jsonify({"messages": load_messanges()})

@app.route('/messages', methods=['POST'])
def post_message():
    data = request.get_json()
    username = data.get("username", "anonim").strip()
    text = data.get("text", "").strip()
    if not text:
       return jsonify({"success": False})
    messages = load_messanges()
    messages.append({"username": username, "text": text})
    save_messages(messages[-100:])
    return jsonify({"success": True})
       
@app.route('/chat')
def chat():
    return render_template('chat.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)              