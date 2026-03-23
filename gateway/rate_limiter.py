# rate_limiter.py - controls how many requests each user can make per minutes
import time

class InMemoryRateLimiter:
    def __init__(self, max_requests=100, window_seconds=60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests = {}
    
    def is_allowed(self, api_key: str):
        now = time.time()
        window_start = now - self.window_seconds
        if api_key not in self._requests:
            self._requests[api_key] = []
        self._requests[api_key] = [
            t for t in self._requests[api_key] if t > window_start
        ]
        self._requests[api_key].append(now)
        current_count = len(self._requests[api_key])
        remaining = max(0, self.max_requests - current_count)
        allowed = current_count <= self.max_requests
        return allowed, current_count, remaining
    
    def get_reset_time(self,api_key: str):
        if api_key not in self._requests or not self._requests[api_key]:
            return 0
        oldest = min(self._requests[api_key])
        return max(0,int(oldest + self.window_seconds - time.time()))
    
    def reset(self, api_key:str):
        self._requests.pop(api_key, None)