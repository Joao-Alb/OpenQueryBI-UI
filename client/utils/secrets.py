import os
from dotenv import load_dotenv, find_dotenv

def load_env():
    _ = load_dotenv(find_dotenv())
    
def get_key(key_name:str):
    load_env()
    key = os.getenv(key_name)
    return key

def has_env_key(key: str) -> bool:
    key = key.upper()
    with open(find_dotenv(), "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith(f"{key}="):
                return True
    return False