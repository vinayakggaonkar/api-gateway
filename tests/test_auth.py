# test_auth.py - Tests for API key authentication
from gateway.auth import verify_api_key, get_user_by_key, VALID_API_KEYS

class TestAuthentication:

    def test_valid_key_returns_user(self):
        user = get_user_by_key("key-alice-abc123")
        assert user is not None
        assert user["username"] == "alice"
        assert user["user_id"] == 1

    def test_invalid_key_returns_none(self):
        user = get_user_by_key("this-is-a-fake-key")
        assert user is None

    def test_all_valid_keys_work(self):
        valid_keys = [
            "key-alice-abc123",
            "key-bob-def456",
            "key-charlie-ghi789",
            "test-api-key-001",
        ]
        for key in valid_keys:
            user = get_user_by_key(key)
            assert user is not None