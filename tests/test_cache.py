# test_cache.py - Tests for response caching
from gateway.cache import InMemoryCache

class TestCache:

    def setup_method(self):
        self.cache = InMemoryCache(ttl=2)
    def test_cache_miss_returns_none(self):
        result = self.cache.get("What is the weather?")
        assert result is None
    def test_cache_stores_and_retrieves(self):
        data = {"intent": "weather", "response": "28C Sunny"}
        self.cache.set("What is the weather?", data)
        result = self.cache.get("What is the weather?")
        assert result is not None
        assert result["intent"] == "weather"
        assert result["response"] == "28C Sunny"
    def test_cache_is_case_insensitive(self):
        data = {"intent": "weather", "response": "28C Sunny"}
        self.cache.set("Weather in Mysuru", data)
        result = self.cache.get("weather in mysuru")
        assert result is not None
    def test_cache_expiry(self):
        import time
        data = {"intent": "finance", "response": "Stock is $100"}
        self.cache.set("Apple stock price", data)
        assert self.cache.get("Apple stock price") is not None
        time.sleep(2.1)
        assert self.cache.get("Apple stock price") is None