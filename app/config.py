from dataclasses import dataclass
from enum import Enum
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class ModelConfig:
    api_key: str
    provider: str

class ChatModel(Enum):
    # Anthropic
    CLAUDE_SONNET_4_6 = "claude-sonnet-4-6"
    CLAUDE_HAIKU_4_5 = "claude-haiku-4-5-20251001"
    CLAUDE_OPUS_4_5 = "claude-opus-4-5"

    # Google
    GEMINI_2_5_FLASH = "gemini-2.5-flash"
    GEMINI_2_5_PRO = "gemini-2.5-pro"
    GEMINI_2_FLASH = "gemini-2.0-flash"

ANTHROPIC_MODELS = {
    ChatModel.CLAUDE_SONNET_4_6,
    ChatModel.CLAUDE_HAIKU_4_5,
    ChatModel.CLAUDE_OPUS_4_5,
}

GOOGLE_MODELS = {
    ChatModel.GEMINI_2_5_FLASH,
    ChatModel.GEMINI_2_5_PRO,
    ChatModel.GEMINI_2_FLASH,
}

class Config:
    @staticmethod
    def get_model_config(model: ChatModel) -> ModelConfig:
        if model in ANTHROPIC_MODELS:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if api_key is None:
                raise ValueError("ANTHROPIC_API_KEY not set")
            return ModelConfig(api_key=api_key, provider="anthropic")

        if model in GOOGLE_MODELS:
            api_key = os.getenv("GOOGLE_API_KEY")
            if api_key is None:
                raise ValueError("GOOGLE_API_KEY not set")
            return ModelConfig(api_key=api_key, provider="google")

        raise ValueError(f"Unknown model: {model}")
