import os
from dotenv import load_dotenv, find_dotenv

def load_env():
    _ = load_dotenv(find_dotenv())
    
def get_key(key_name:str):
    load_env()
    key = os.getenv(key_name)
    return key