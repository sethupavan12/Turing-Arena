import time
from collections import OrderedDict
from azure.storage.blob import BlobServiceClient, ContainerClient

from collections import OrderedDict
from azure.storage.blob import BlobServiceClient
import time

class LRUCache:
    """
    A class representing a Least Recently Used (LRU) cache.

    Attributes:
        cache (OrderedDict): The cache data structure.
        capacity (int): The maximum number of items the cache can hold.
        blob_service_client (BlobServiceClient): The BlobServiceClient object for interacting with Azure Blob Storage.
        container_client (ContainerClient): The ContainerClient object for accessing the container in Azure Blob Storage.
    """

    def __init__(self, capacity: int, connection_string: str, container_name: str):
        """
        Initializes a new instance of the LRUCache class.

        Args:
            capacity (int): The maximum number of items the cache can hold.
            connection_string (str): The connection string for accessing Azure Blob Storage.
            container_name (str): The name of the container in Azure Blob Storage.
        """
        self.cache = OrderedDict()
        self.capacity = capacity
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_client = self.blob_service_client.get_container_client(container_name)

    def get(self, model: str, key: str):
        """
        Retrieves the value associated with the given model and key from the cache.

        Args:
            model (str): The model name.
            key (str): The key associated with the value.

        Returns:
            The value associated with the given model and key, or None if not found in the cache.
        """
        full_key = f"{model}:{key}"
        if full_key not in self.cache:
            return None
        value = self.cache.pop(full_key)
        self.cache[full_key] = value
        return value

    def put(self, model: str, key: str, value: str):
        """
        Adds or updates the value associated with the given model and key in the cache.

        Args:
            model (str): The model name.
            key (str): The key associated with the value.
            value (str): The value to be added or updated.
        """
        full_key = f"{model}:{key}"
        if full_key in self.cache:
            self.cache.pop(full_key)
        elif len(self.cache) >= self.capacity:
            oldest_key, oldest_value = self.cache.popitem(last=False)
            self.offload_to_blob(oldest_key, oldest_value)
        self.cache[full_key] = value

    def offload_to_blob(self, key: str, value: str):
        """
        Offloads the given key-value pair to Azure Blob Storage.

        Args:
            key (str): The key associated with the value.
            value (str): The value to be offloaded.
        """
        blob_client = self.container_client.get_blob_client(key)
        blob_client.upload_blob(value, overwrite=True)

    def delete_old_blobs(self, retention_period: int):
        """
        Deletes the old blobs from Azure Blob Storage based on the retention period.

        Args:
            retention_period (int): The retention period in seconds.
        """
        blobs = self.container_client.list_blobs()
        for blob in blobs:
            blob_client = self.container_client.get_blob_client(blob)
            properties = blob_client.get_blob_properties()
            if time.time() - properties['last_modified'].timestamp() > retention_period:
                blob_client.delete_blob()