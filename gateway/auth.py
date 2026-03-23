# auth.py - checks API keys for every incoming requests
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# our valid API keys dictionary
VALID_API_KEYS = {
    "key-alice-abc123":    {"user_id":1, "username":"alice"},
    "key-bob-def456":      {"user_id":2, "username":"bob"},
    "key-charlie-ghi789":  {"user_id":3, "username":"charlie"},
    "test-api-key-001":    {"user_id":4, "username":"testuser"},
}

# now the main function that checks the API key
def verify_api_key(api_key: str = Security(api_key_header)) -> dict:
    if not api_key:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Missing API key. Add header: X-API-Key: <Your-key>",
        )
    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key.",
        )
    return VALID_API_KEYS[api_key]

def get_user_by_key(api_key: str):
    return VALID_API_KEYS.get(api_key)