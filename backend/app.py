import os
import requests
from flask import Flask, request, Response, send_from_directory
from flask_cors import CORS
from azure.storage.blob import BlobServiceClient
import json
import hashlib
from cache import LRUCache

app = Flask(__name__)
CORS(app)

OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"

# Azure Blob Storage configuration
AZURE_CONNECTION_STRING = os.getenv('AZURE_CONNECTION_STRING')
CONTAINER_NAME = 'cache'

# Initialize LRUCache
cache = LRUCache(capacity=10, connection_string=AZURE_CONNECTION_STRING, container_name=CONTAINER_NAME)

def get_cache_key(user_input):
    return hashlib.md5(user_input.encode()).hexdigest()

def get_from_cache(model, key):
    # Check in-memory cache
    cached_response = cache.get(model, key)
    if cached_response:
        return cached_response
    
    # Check Azure Blob Storage
    try:
        blob_client = cache.container_client.get_blob_client(f"{model}:{key}")
        blob_data = blob_client.download_blob().readall()
        return blob_data.decode('utf-8')
    except Exception as e:
        return None

def save_to_cache(model, key, data):
    # Save to in-memory cache
    cache.put(model, key, data)

# Serve static content
@app.route('/')
def serve_static():
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:path>')
def serve_static_files(path):
    return send_from_directory('static', path)

# Chat endpoint for LLM 1
@app.route('/chat_llm1', methods=['POST'])
def chat_llm1():
    LLM1="phi3"
    data = request.json
    user_input = data.get('user_input')
    cache_key = get_cache_key(user_input)
    
    cached_response = get_from_cache(LLM1, cache_key)
    if cached_response:
        return Response(cached_response, content_type='text/event-stream')
    
    def generate():
        payload = {
            "model": LLM1,
            "prompt": user_input
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(OLLAMA_GENERATE_URL, json=payload, headers=headers, stream=True)
        
        response_data = ""
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                chunk_data = chunk.decode('utf-8')
                response_data += chunk_data
                yield chunk_data
        
        save_to_cache(LLM1, cache_key, response_data)
    
    return Response(generate(), content_type='text/event-stream')

# Chat endpoint for LLM 2
@app.route('/chat_llm2', methods=['POST'])
def chat_llm2():
    LLM2="llama3.1"
    data = request.json
    user_input = data.get('user_input')
    cache_key = get_cache_key(user_input)
    
    cached_response = get_from_cache(LLM2, cache_key)
    if cached_response:
        return Response(cached_response, content_type='text/event-stream')
    
    def generate():
        payload = {
            "model": LLM2,
            "prompt": user_input
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(OLLAMA_GENERATE_URL, json=payload, headers=headers, stream=True)
        
        response_data = ""
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                chunk_data = chunk.decode('utf-8')
                response_data += chunk_data
                yield chunk_data
        
        save_to_cache(LLM2, cache_key, response_data)
    
    return Response(generate(), content_type='text/event-stream')

# Endpoint to store votes
@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    llm = data.get('llm')
    vote_data = json.dumps(data)
    # Store vote_data as needed
    return "Vote received", 200

if __name__ == '__main__':
    app.run(debug=True)