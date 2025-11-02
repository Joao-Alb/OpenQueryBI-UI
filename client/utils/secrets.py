import os
from dotenv import load_dotenv, find_dotenv

def load_env():
    dotenv_path = find_dotenv()
    if dotenv_path:
        load_dotenv(dotenv_path)

def get_key(key_name: str) -> str | None:
    load_env()
    return os.getenv(key_name)

def has_env_key(key: str) -> bool:
    key = key.upper()
    if key in os.environ:
        return True
    dotenv_path = find_dotenv()
    if dotenv_path and os.path.exists(dotenv_path):
        with open(dotenv_path, "r") as f:
            for line in f:
                if line.strip().startswith(f"{key}="):
                    return True
    return False
