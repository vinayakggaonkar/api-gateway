# cache.py - stores responses so we don't call the same service twice

import time
import hashlib
import json
from typing import Optional

# cache class
class InMemoryCache:
    def __init__(self, ttl=30):
        self.ttl = ttl
        self._store = {}
    
    def _make_key(self, query:str) -> str:
        normalized = query.lower().strip()
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def get(self, query:str) -> Optional[dict]:
        key = self._make_key(query)
        if key not in self._store:
            return None
        entry = self._store[key]
        if time.time() > entry["expires_at"]:
            del self._store[key]
            return None
        return entry["data"]
    
    def set(self, query: str, response_data: dict) -> None:
        key = self._make_key(query)
        self._store[key] = {
            "data": response_data,
            "expires_at": time.time() + self.ttl
        }

    def delete(self, query: str) -> None:
        key = self._make_key(query)
        self._store.pop(key, None)

    def flush_all(self) -> None:
        self._store.clear()