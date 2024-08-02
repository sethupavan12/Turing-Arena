import React, { useState, useEffect } from 'react';
import {
    AppBar,
    Toolbar,
    Typography,
    Container,
    TextField,
    Paper,
    Box,
    Grid,
    CircularProgress,
} from '@mui/material';
import './App.css';

function App() {
    const [topic, setTopic] = useState('Turing Arena');
    const [message, setMessage] = useState('');
    const [chatA, setChatA] = useState([]);
    const [chatB, setChatB] = useState([]);
    const [vote, setVote] = useState('');
    const [leaderboard, setLeaderboard] = useState({});
    const [loadingA, setLoadingA] = useState(false);
    const [loadingB, setLoadingB] = useState(false);

    useEffect(() => {
        // Simulate fetching topic
        setTopic('Turing Arena');
    }, []);

    const handleResponse = () => {
        setLoadingA(true);
        setLoadingB(true);
        const userMessage = { sender: 'user', text: message };
        setChatA([...chatA, userMessage]);
        setChatB([...chatB, userMessage]);

        setTimeout(() => {
            const aiMessageA = { sender: 'ai', text: 'Dummy response from AI 1' };
            setChatA([...chatA, userMessage, aiMessageA]);
            setLoadingA(false);
        }, 1000);

        setTimeout(() => {
            const aiMessageB = { sender: 'ai', text: 'Dummy response from AI 2' };
            setChatB([...chatB, userMessage, aiMessageB]);
            setLoadingB(false);
        }, 1000);

        setMessage('');
    };

    const handleVote = () => {
        setVote('');
        setChatA([]);
        setChatB([]);
        setMessage('');
        // Simulate submitting vote
        console.log('Vote submitted:', vote);
    };

    const fetchLeaderboard = () => {
        // Simulate fetching leaderboard
        setLeaderboard({
            AI_1: 10,
            AI_2: 15,
            Tie: 5,
            Both_Bad: 2,
        });
    };

    const renderChat = (chat) => (
        chat.map((msg, index) => (
            <Box
                key={index}
                display="flex"
                justifyContent={msg.sender === 'user' ? 'flex-end' : 'flex-start'}
                my={1}
            >
                <Paper
                    elevation={3}
                    style={{
                        padding: '8px 16px',
                        backgroundColor: msg.sender === 'user' ? '#dcf8c6' : '#ffffff',
                        maxWidth: '60%',
                    }}
                >
                    <Typography variant="body1">{msg.text}</Typography>
                </Paper>
            </Box>
        ))
    );

    return (
        <div>
            <div className="wave-background" />
            <AppBar position="static" className="App-header">
                <Toolbar>
                    <Typography variant="h6">Turing Arena</Typography>
                </Toolbar>
            </AppBar>
            <Container className="main-container">
                <Box my={4}>
                    <Typography variant="h4" align="center" gutterBottom>
                        {topic}
                    </Typography>
                    <Grid container spacing={2} justifyContent="center">
                        <Grid item xs={12} md={6}>
                            <Paper elevation={3} className="chat-window glowing-border" style={{ padding: '16px' }}>
                                <Typography variant="h6">Chat with AI 1</Typography>
                                <Box className="chat-content">
                                    {loadingA && (
                                        <Box display="flex" justifyContent="center" my={4}>
                                            <CircularProgress style={{ color: '#ffffff' }} />
                                        </Box>
                                    )}
                                    {renderChat(chatA)}
                                </Box>
                            </Paper>
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <Paper elevation={3} className="chat-window glowing-border" style={{ padding: '16px' }}>
                                <Typography variant="h6">Chat with AI 2</Typography>
                                <Box className="chat-content">
                                    {loadingB && (
                                        <Box display="flex" justifyContent="center" my={4}>
                                            <CircularProgress style={{ color: '#ffffff' }} />
                                        </Box>
                                    )}
                                    {renderChat(chatB)}
                                </Box>
                            </Paper>
                        </Grid>
                        <Grid item xs={12} md={12}>
                            <Paper elevation={3} className="paper glowing-border" style={{ padding: '16px', marginTop: '16px' }}>
                                <TextField
                                    fullWidth
                                    label="Your message"
                                    value={message}
                                    onChange={(e) => setMessage(e.target.value)}
                                    variant="outlined"
                                    multiline
                                    rows={2}
                                    InputLabelProps={{ style: { color: '#000000' } }}
                                    InputProps={{ style: { color: '#000000' } }}
                                />
                                <Box mt={2} display="flex" justifyContent="center">
                                    <button
                                        onClick={handleResponse}
                                        className="custom-button custom-button-primary"
                                    >
                                        Submit
                                    </button>
                                </Box>
                            </Paper>
                        </Grid>
                        <Grid item xs={12} md={12}>
                            <Box mt={2} display="flex" justifyContent="space-between">
                                <button
                                    onClick={() => setVote('AI_1')}
                                    className="custom-button custom-button-success"
                                >
                                    Vote AI 1
                                </button>
                                <button
                                    onClick={() => setVote('AI_2')}
                                    className="custom-button custom-button-success"
                                >
                                    Vote AI 2
                                </button>
                                <button
                                    onClick={() => setVote('tie')}
                                    className="custom-button custom-button-secondary"
                                >
                                    Tie
                                </button>
                                <button
                                    onClick={() => setVote('both_bad')}
                                    className="custom-button custom-button-secondary"
                                >
                                    Both are Bad
                                </button>
                                <button
                                    onClick={handleVote}
                                    className="custom-button custom-button-primary"
                                >
                                    Submit Vote
                                </button>
                            </Box>
                        </Grid>
                        <Grid item xs={12} md={12}>
                            <button
                                onClick={fetchLeaderboard}
                                className="custom-button custom-button-leaderboard"
                            >
                                Show Leaderboard
                            </button>
                            {Object.keys(leaderboard).length > 0 && (
                                <Paper elevation={3} className="paper" style={{ padding: '16px', marginTop: '16px' }}>
                                    <Typography variant="h6">Leaderboard</Typography>
                                    <Typography variant="body1" className="leaderboard">
                                        {JSON.stringify(leaderboard, null, 2)}
                                    </Typography>
                                </Paper>
                            )}
                        </Grid>
                    </Grid>
                </Box>
            </Container>
        </div>
    );
}

export default App;
