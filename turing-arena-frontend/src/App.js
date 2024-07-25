// src/App.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
    AppBar,
    Toolbar,
    Typography,
    Container,
    TextField,
    Button,
    Paper,
    Box,
    Grid,
    CircularProgress,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import ThumbDownIcon from '@mui/icons-material/ThumbDown';
import './App.css';

function App() {
    const [topic, setTopic] = useState('');
    const [message, setMessage] = useState('');
    const [response, setResponse] = useState('');
    const [vote, setVote] = useState('');
    const [leaderboard, setLeaderboard] = useState({});
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        axios.get('http://localhost:5000/get_topic')
            .then(res => {
                setTopic(res.data.topic);
            });
    }, []);

    const handleResponse = (responder) => {
        setLoading(true);
        axios.post('http://localhost:5000/get_response', { message, responder })
            .then(res => {
                setResponse(res.data.response);
                setLoading(false);
            });
    };

    const handleVote = () => {
        axios.post('http://localhost:5000/submit_vote', { responder: 'AI_1', vote })
            .then(res => {
                setVote('');
                setResponse('');
                setMessage('');
            });
    };

    const fetchLeaderboard = () => {
        axios.get('http://localhost:5000/leaderboard')
            .then(res => {
                setLeaderboard(res.data);
            });
    };

    return (
        <div>
            <div className="wave-background" />
            <AppBar position="static" className="App-header">
                <Toolbar>
                    <Typography variant="h6">Turing Arena</Typography>
                </Toolbar>
            </AppBar>
            <Container>
                <Box my={4}>
                    <Typography variant="h4" align="center" gutterBottom>
                        {topic}
                    </Typography>
                    <Grid container spacing={2} justifyContent="center">
                        <Grid item xs={12} md={8}>
                            <Paper elevation={3} className="paper" style={{ padding: '16px' }}>
                                <TextField
                                    fullWidth
                                    label="Your message"
                                    value={message}
                                    onChange={(e) => setMessage(e.target.value)}
                                    variant="outlined"
                                    multiline
                                    rows={4}
                                    InputLabelProps={{ style: { color: '#000000' } }}
                                    InputProps={{ style: { color: '#000000' } }}
                                />
                                <Box mt={2} display="flex" justifyContent="space-between">
                                    <Button
                                        variant="contained"
                                        color="primary"
                                        endIcon={<SendIcon />}
                                        onClick={() => handleResponse('AI_1')}
                                        className="custom-button custom-button-primary"
                                    >
                                        Talk to AI 1
                                    </Button>
                                    <Button
                                        variant="contained"
                                        color="secondary"
                                        endIcon={<SendIcon />}
                                        onClick={() => handleResponse('AI_2')}
                                        className="custom-button custom-button-secondary"
                                    >
                                        Talk to AI 2
                                    </Button>
                                    <Button
                                        variant="contained"
                                        endIcon={<SendIcon />}
                                        onClick={() => handleResponse('human')}
                                        className="custom-button custom-button-success"
                                    >
                                        Talk to Human
                                    </Button>
                                </Box>
                            </Paper>
                        </Grid>
                        <Grid item xs={12} md={8}>
                            {loading ? (
                                <Box display="flex" justifyContent="center" my={4}>
                                    <CircularProgress style={{ color: '#ffffff' }} />
                                </Box>
                            ) : (
                                response && (
                                    <Paper elevation={3} className="paper" style={{ padding: '16px', marginTop: '16px' }}>
                                        <Typography variant="h6">Response:</Typography>
                                        <Typography variant="body1" style={{ marginTop: '8px' }}>
                                            {response}
                                        </Typography>
                                        <Box mt={2} display="flex" justifyContent="space-between">
                                            <Button
                                                variant="outlined"
                                                color="primary"
                                                startIcon={<ThumbUpIcon />}
                                                onClick={() => setVote('human')}
                                                className="custom-button custom-button-success"
                                            >
                                                Vote Human
                                            </Button>
                                            <Button
                                                variant="outlined"
                                                color="secondary"
                                                startIcon={<ThumbDownIcon />}
                                                onClick={() => setVote('ai')}
                                                className="custom-button custom-button-secondary"
                                            >
                                                Vote AI
                                            </Button>
                                            <Button
                                                variant="contained"
                                                color="primary"
                                                onClick={handleVote}
                                                className="custom-button custom-button-primary"
                                            >
                                                Submit Vote
                                            </Button>
                                        </Box>
                                    </Paper>
                                )
                            )}
                        </Grid>
                        <Grid item xs={12} md={8}>
                            <Button
                                variant="contained"
                                color="primary"
                                onClick={fetchLeaderboard}
                                fullWidth
                                className="custom-button custom-button-leaderboard"
                            >
                                Show Leaderboard
                            </Button>
                            {leaderboard && (
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
