import pytest
from cache import LRUCache
from unittest.mock import MagicMock

@pytest.fixture
def cache():
    connection_string = "fake_connection_string"
    container_name = "test_container"
    return LRUCache(capacity=2, connection_string=connection_string, container_name=container_name)

def test_cache_put_and_get(cache):
    cache.put("Phi3", "key1", "value1")
    assert cache.get("Phi3", "key1") == "value1"

    cache.put("Llama3.1", "key2", "value2")
    assert cache.get("Llama3.1", "key2") == "value2"

    cache.put("Phi3", "key3", "value3")
    assert cache.get("Phi3", "key1") is None  # key1 should be evicted
    assert cache.get("Phi3", "key3") == "value3"

def test_cache_eviction(cache):
    cache.put("Phi3", "key1", "value1")
    cache.put("Phi3", "key2", "value2")
    cache.put("Phi3", "key3", "value3")  # This should evict key1

    assert cache.get("Phi3", "key1") is None
    assert cache.get("Phi3", "key2") == "value2"
    assert cache.get("Phi3", "key3") == "value3"

def test_offload_to_blob(cache):
    cache.offload_to_blob = MagicMock()
    cache.put("Phi3", "key1", "value1")
    cache.put("Phi3", "key2", "value2")
    cache.put("Phi3", "key3", "value3")  # This should trigger offload_to_blob

    cache.offload_to_blob.assert_called_once_with("Phi3:key1", "value1")