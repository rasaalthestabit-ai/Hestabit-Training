import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

LLM_CONFIG = {
    "config_list": [
        {
            "model": GROQ_MODEL,
            "base_url": "https://api.groq.com/openai/v1",
            "api_key": GROQ_API_KEY,
            "price": [0.0, 0.0]
        }
    ],
    "temperature": 0.5,
    "cache_seed": None,
}