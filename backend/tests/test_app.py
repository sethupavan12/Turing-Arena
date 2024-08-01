import pytest
from app import app, get_cache_key, get_from_cache, save_to_cache
from cache import LRUCache
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def cache():
    connection_string = "fake_connection_string"
    container_name = "test_container"
    return LRUCache(capacity=2, connection_string=connection_string, container_name=container_name)

def test_get_cache_key():
    assert get_cache_key("test_input") == "d5579c46dfcc7d0d5fc0a9b3d3c9e0f3"

@patch('app.cache')
def test_get_from_cache(mock_cache):
    mock_cache.get.return_value = "cached_response"
    assert get_from_cache("Phi3", "test_key") == "cached_response"

@patch('app.cache')
def test_save_to_cache(mock_cache):
    save_to_cache("Phi3", "test_key", "test_data")
    mock_cache.put.assert_called_once_with("Phi3", "test_key", "test_data")

@patch('app.get_from_cache')
@patch('app.save_to_cache')
@patch('requests.post')
def test_chat_llm1(mock_post, mock_save_to_cache, mock_get_from_cache, client):
    mock_get_from_cache.return_value = None
    mock_post.return_value.iter_content = MagicMock(return_value=[b"response_chunk"])
    
    response = client.post('/chat_llm1', json={'user_input': 'test_input'})
    assert response.status_code == 200
    assert b"response_chunk" in response.data

@patch('app.get_from_cache')
@patch('app.save_to_cache')
@patch('requests.post')
def test_chat_llm2(mock_post, mock_save_to_cache, mock_get_from_cache, client):
    mock_get_from_cache.return_value = None
    mock_post.return_value.iter_content = MagicMock(return_value=[b"response_chunk"])
    
    response = client.post('/chat_llm2', json={'user_input': 'test_input'})
    assert response.status_code == 200
    assert b"response_chunk" in response.data

def test_vote(client):
    response = client.post('/vote', json={'llm': 'Phi3', 'vote': 'up'})
    assert response.status_code == 200
    assert response.data == b"Vote received"