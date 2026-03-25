from app.config import ChatModel, Config
from langchain.chat_models import init_chat_model

class RagEngine:
    def __init__(self, config_service: Config):
       self.config_service = config_service

       api_key = self.config_service.get_model_config(ChatModel.CLAUDE_HAIKU_4_5).api_key

       self.chat_model = init_chat_model(api_key)
