import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Fetch environment variables with safe defaults
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "smollm:135m")
APP_API_KEY = os.getenv("APP_API_KEY", "local-dev-key")

# Safely parse requested timeout
_timeout_str = os.getenv("REQUEST_TIMEOUT", "120")
try:
    REQUEST_TIMEOUT = int(_timeout_str)
except ValueError:
    REQUEST_TIMEOUT = 120
