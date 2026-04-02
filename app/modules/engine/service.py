from app.config import ChatModel, Config, EmbeddingModels
from langchain.chat_models import init_chat_model
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

class RagEngine:
    def __init__(
        self,
        config_service: Config,
        collection_name: str
    ):
       self.config_service = config_service

       self.chat_model = init_chat_model(model=str(ChatModel.CLAUDE_HAIKU_4_5))
       self.embedding_model = GoogleGenerativeAIEmbeddings(model=f"models/{EmbeddingModels.GEMINI_001}")
       self.vector_store = Chroma(
           collection_name=collection_name,
           embedding_function=self.embedding_model,
           persist_directory="./chroma_langchain_db",
       )
