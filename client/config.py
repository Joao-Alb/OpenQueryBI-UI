import os
import json
from dotenv import load_dotenv
from utils.secrets import has_env_key

load_dotenv()
env = os.getenv

# Model mapping
MODEL_OPTIONS = {
    'Anthropic': 'claude-3-5-sonnet-20240620',
    'OpenAI': 'gpt-5-nano',
    'Google': 'gemini-2.0-flash-001',
    'Bedrock': 'us.anthropic.claude-3-7-sonnet-20250219-v1:0'
    }

#list only the providers that are available in the config file
AVAILABLE_PROVIDERS = [provider for provider in MODEL_OPTIONS.keys() if (has_env_key(provider) or provider == "Bedrock")]

# Streamlit defaults
DEFAULT_MAX_TOKENS = 4096
DEFAULT_TEMPERATURE = 0.2

# Load server configuration
config_path = os.path.join('.', 'servers_config.json')
if os.path.exists(config_path):
    with open(config_path, 'r') as f:
        SERVER_CONFIG = json.load(f)