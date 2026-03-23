# test_rate_limiter.py - Tests for rate limiting
from gateway.rate_limiter import InMemoryRateLimiter

class TestRateLimiter:

    def setup_method(self):
        self.limiter = InMemoryRateLimiter(max_requests=5, window_seconds=60)

    def test_first_request_is_allowed(self):
        allowed, count, remaining = self.limiter.is_allowed("test-key")
        assert allowed is True
        assert count == 1
        assert remaining == 4

    def test_request_over_limit_is_blocked(self):
        for _ in range(5):
            self.limiter.is_allowed("test-key")
        allowed, count, remaining = self.limiter.is_allowed("test-key")
        assert allowed is False
        assert remaining == 0

    def test_reset_clears_counter(self):
        for _ in range(5):
            self.limiter.is_allowed("test-key")
        allowed, _, _ = self.limiter.is_allowed("test-key")
        assert allowed is False
        self.limiter.reset("test-key")
        allowed, count, _ = self.limiter.is_allowed("test-key")
        assert allowed is True
        assert count == 1

    def test_different_keys_are_independent(self):
        for _ in range(5):
            self.limiter.is_allowed("alice-key")
        allowed_alice, _, _ = self.limiter.is_allowed("alice-key")
        allowed_bob, count_bob, _ = self.limiter.is_allowed("bob-key")
        assert allowed_alice is False
        assert allowed_bob is True
        assert count_bob == 1
