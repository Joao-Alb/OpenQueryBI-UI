import os
from dotenv import load_dotenv, find_dotenv

def get_env_path():
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    env_path = os.path.join(parent_dir, '.env')
    return env_path if os.path.exists(env_path) else find_dotenv()

def load_env():
    _ = load_dotenv(get_env_path())

def get_key(key_name: str):
    load_env()
    key = os.getenv(key_name)
    return key

def has_env_key(key: str) -> bool:
    key = key.upper()
    env_path = get_env_path()
    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith(f"{key}="):
                return True
    return False