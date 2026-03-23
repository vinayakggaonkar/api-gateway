# config.py - All settings for our API Gateway live here

import os
class Settings:
    REDIS_HOST = os.getenv("REDIS_HOST","localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT","6379"))
    MYSQL_HOST = os.getenv("MYSQL_HOST","localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT","3306"))
    MYSQL_USER = os.getenv("MYSQL_USER","gateway_user")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD","gateway_pass")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE","gateway_db")
    RATE_LIMIT_REQUESTS = 100
    RATE_LIMIT_WINDOW_SEC = 60
    CACHE_TTL_SEC = 30
    GATEWAY_HOST = "0.0.0.0"
    GATEWAY_PORT = 8000

settings = Settings()


