# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Dummy data for leaderboard
leaderboard = {
    'Phi3': {'human_votes': 0, 'total_votes': 0},
    '': {'human_votes': 0, 'total_votes': 0}
}


# We need to basically 
# 1. Generate a random topic to talk about, provoking a question, from an LLM or human
# 2. Once we get a random topic question, we then  send that question to LLM if its LLM's turn (we make sure at random that user gets first changes or AI)
# 3. If it is user's turn we wait for user's answer and then send that to LLM and relay the reply
# 4. Once a two and fro conv Ai replies to human or human replies to AI is done, we then say end of chat.
# 5. Ask for Vote if it is human or AI
# 6. Send the vote to DB for safe keeping along with caching the question asked by human, question asked by AI, random topic generated
# 7. Next time another user comes in, the random topic is randomly returned from the cache along with AI question or human

@app.route('/get_topic', methods=['GET'])
def get_topic():
    topic = "Discuss the implications of AI in modern society."
    return jsonify({'topic': topic})

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.json
    message = data.get('message')
    responder = data.get('responder')  # 'AI_1', 'AI_2' or 'human'

    # Simulate response
    if responder == 'AI_1':
        response = "AI_1's response to: " + message
    elif responder == 'AI_2':
        response = "AI_2's response to: " + message
    else:
        response = "Human's response to: " + message

    return jsonify({'response': response})

@app.route('/submit_vote', methods=['POST'])
def submit_vote():
    data = request.json
    responder = data.get('responder')
    vote = data.get('vote')  # 'human' or 'ai'

    if responder in leaderboard:
        leaderboard[responder]['total_votes'] += 1
        if vote == 'human':
            leaderboard[responder]['human_votes'] += 1

    return jsonify({'status': 'success'})

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    human_likeness = {key: (value['human_votes'] / value['total_votes']) * 100 if value['total_votes'] > 0 else 0 for key, value in leaderboard.items()}
    return jsonify(human_likeness)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
