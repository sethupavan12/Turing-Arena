from flask import Flask, request, jsonify
from flask_socketio import SocketIO, send, emit
from flask_sqlalchemy import SQLAlchemy
import random
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'nokeyset')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
socketio = SocketIO(app)

from models import Vote

users = {}
available_users = []

# Dummy LLM responses for demonstration
llm_responses = [
    "Hello! How can I help you today?",
    "I'm just a chatbot, but I'll do my best to assist you.",
    "Can you tell me more about that?",
    "That's interesting. Tell me more.",
    "How can I help you further?"
]

@app.route('/')
def index():
    return "Chat App Backend"

@app.route('/submit-vote', methods=['POST'])
def submit_vote():
    data = request.json
    vote = Vote(session_id=data['session_id'], is_human=data['is_human'])
    db.session.add(vote)
    db.session.commit()
    return jsonify({"message": "Vote submitted successfully"}), 201

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    results = db.session.query(Vote.is_human, db.func.count(Vote.id)).group_by(Vote.is_human).all()
    leaderboard_data = [{"is_human": result[0], "count": result[1]} for result in results]
    return jsonify({"leaderboard": leaderboard_data})

@socketio.on('connect')
def handle_connect():
    users[request.sid] = None
    available_users.append(request.sid)
    print(f'User {request.sid} connected.')

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in users:
        partner_sid = users[request.sid]
        if partner_sid in users:
            users[partner_sid] = None
            available_users.append(partner_sid)
        del users[request.sid]
    if request.sid in available_users:
        available_users.remove(request.sid)
    print(f'User {request.sid} disconnected.')

@socketio.on('message')
def handle_message(message):
    sid = request.sid
    if users[sid] is None:
        if available_users and len(available_users) > 1:
            partner_sid = available_users.pop(0)
            if partner_sid != sid:
                users[sid] = partner_sid
                users[partner_sid] = sid
                send({"user": "System", "text": "You are now connected to another user."}, to=sid)
                send({"user": "System", "text": "You are now connected to another user."}, to=partner_sid)
            else:
                available_users.append(sid)
        else:
            send({"user": "System", "text": "You are now chatting with an AI."}, to=sid)
            users[sid] = 'AI'
    if users[sid] == 'AI':
        response = random.choice(llm_responses)
        send({"user": "AI", "text": response}, to=sid)
    else:
        partner_sid = users[sid]
        send({"user": "User", "text": message}, to=partner_sid)

if __name__ == '__main__':
    db.create_all()
    socketio.run(app, debug=True)
