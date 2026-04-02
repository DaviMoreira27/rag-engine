import pytest

from app.config import ChatModel, Config


def test_get_anthropic_api_key_returns_value():
    key = Config.get_model_config(ChatModel.CLAUDE_SONNET_4_6)

    assert key.provider == "anthropic"


# monkeypatch is fixture provided by default
def test_get_anthropic_api_key_raises_when_missing(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    with pytest.raises(ValueError, match="ANTHROPIC_API_KEY not set"):
        Config.get_model_config(ChatModel.CLAUDE_SONNET_4_6)


def test_get_google_api_key_returns_value():
    key = Config.get_model_config(ChatModel.GEMINI_2_5_FLASH)

    assert key.provider == "google"


def test_get_google_api_key_raises_when_missing(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)

    with pytest.raises(ValueError, match="GOOGLE_API_KEY not set"):
        Config.get_model_config(ChatModel.GEMINI_2_5_FLASH)
