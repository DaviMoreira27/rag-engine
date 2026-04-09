from dataclasses import dataclass
from enum import Enum
from typing import Set

class Environment(Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"

@dataclass
class ModelConfig:
    api_key: str
    provider: str
    model: str

class ChatModels(Enum):
    # Anthropic
    CLAUDE_SONNET_4_6 = "claude-sonnet-4-6"
    CLAUDE_HAIKU_4_5 = "claude-haiku-4-5-20251001"
    CLAUDE_OPUS_4_5 = "claude-opus-4-5"

    # Google
    GEMINI_2_5_FLASH = "gemini-2.5-flash"
    GEMINI_2_5_PRO = "gemini-2.5-pro"
    GEMINI_2_FLASH = "gemini-2.0-flash"

class EmbeddingModels (Enum):
    # Google
    GEMINI_001 = "gemini-embedding-001"


ANTHROPIC_MODELS = {
    ChatModels.CLAUDE_SONNET_4_6,
    ChatModels.CLAUDE_HAIKU_4_5,
    ChatModels.CLAUDE_OPUS_4_5,
}

type UnionGoogleModels = ChatModels | EmbeddingModels

GOOGLE_MODELS: Set[UnionGoogleModels] = {
    ChatModels.GEMINI_2_5_FLASH,
    ChatModels.GEMINI_2_5_PRO,
    ChatModels.GEMINI_2_FLASH,
    EmbeddingModels.GEMINI_001
}

PROVIDER_MAP = {
    **{model: "anthropic" for model in ANTHROPIC_MODELS},
    **{model: "google" for model in GOOGLE_MODELS},
}

@dataclass
class RedisConfig:
    host: str
    port: int
    username: str
    password: str
    max_connections: int
