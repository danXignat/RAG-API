from llama_index.core.memory import ChatMemoryBuffer
from uuid import uuid4, UUID

from services import Globals

def create_chat() -> str:
    """"Creates new chat in Globals.CHATS from services"""
    id = str(uuid4())
    
    ChatMemoryBuffer.from_defaults(
        chat_store=Globals.CHATS,
        chat_store_key=id
    )
    
    return id