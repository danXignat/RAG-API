from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_parse import LlamaParse
from llama_index.core.llms import ChatMessage, MessageRole

from typing import Dict
from dotenv import load_dotenv
import os

from config.settings import LLM_MODEL_NAME, EMBED_MODEL_NAME

load_dotenv()    

class Globals:
    LLM: Ollama = Ollama(model=LLM_MODEL_NAME, request_timeout=240, temperature=0.9)
    
    EMBED_MODEL: HuggingFaceEmbedding = HuggingFaceEmbedding(model_name=EMBED_MODEL_NAME)
    
    PARSER: LlamaParse = LlamaParse(api_key=os.environ["LLAMA_CLOUD_API_KEY"], result_type="markdown")
        
    CHATS: SimpleChatStore = SimpleChatStore()
    
    @staticmethod
    def add_message(chat_id: str, role: str, message: str) -> None:
        """
        Adding a message to a specified session with a specified role
        Args:
            chat_id (str): id session
            role (str): "user" | "assistant" supported
            message (str): content
        """
        chat_role = None
        if role == "user":
            chat_role = MessageRole.USER
        elif role == "assistant":
            chat_role = MessageRole.ASSISTANT
            
        chat_message = ChatMessage(role=chat_role, content=message)
        
        Globals.CHATS.add_message(key=chat_id, message=chat_message)
    
    

