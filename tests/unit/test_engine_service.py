import pytest
from app.config import Config

def test_get_anthropic_api_key_returns_value(monkeypatch):
    key = Config.get_anthropic_api_key()

    assert key == "something"

def test_get_anthropic_api_key_raises_when_missing(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    with pytest.raises(ValueError, match="ANTHROPIC_API_KEY not set"):
        Config.get_anthropic_api_key()
