import os

def get_env(key, fallback):
    env = os.getenv(key, default=fallback)
    return env