import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    @staticmethod
    def get_anthropic_api_key() -> str:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if api_key is None:
            raise ValueError("ANTHROPIC_API_KEY not set")
        return api_key
