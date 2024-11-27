# config.py
import os


class Settings:
    PROXY_POOL_URL = os.getenv("PROXY_POOL_URL", "http://81.68.212.127:5010")


settings = Settings()
