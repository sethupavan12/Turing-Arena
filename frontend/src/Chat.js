import React, { useState } from 'react';
import io from 'socket.io-client';

const socket = io('http://localhost:5000');

function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [questionCount, setQuestionCount] = useState(0);
  const [sessionId, setSessionId] = useState(Math.random().toString(36).substring(2, 15));

  socket.on('message', (msg) => {
    setMessages((prevMessages) => [...prevMessages, msg]);
  });

  const sendMessage = () => {
    if (input.trim() && questionCount < 5) {
      socket.emit('message', input);
      setMessages((prevMessages) => [...prevMessages, { user: 'You', text: input }]);
      setInput('');
      setQuestionCount(questionCount + 1);
    }
  };

  const submitVote = (isHuman) => {
    fetch('http://localhost:5000/submit-vote', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ session_id: sessionId, is_human: isHuman })
    }).then(response => response.json())
      .then(data => {
        alert(data.message);
      });
  };

  const showLeaderboard = () => {
    fetch('http://localhost:5000/leaderboard')
      .then(response => response.json())
      .then(data => {
        alert(JSON.stringify(data.leaderboard));
      });
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, index) => (
          <div key={index} className="message">
            <strong>{msg.user}: </strong> {msg.text}
          </div>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type your message..."
      />
      <button onClick={sendMessage} disabled={questionCount >= 5}>Send</button>
      <div>
        <button onClick={() => submitVote(true)}>Vote Human</button>
        <button onClick={() => submitVote(false)}>Vote AI</button>
        <button onClick={showLeaderboard}>Show Leaderboard</button>
      </div>
    </div>
  );
}

export default Chat;
