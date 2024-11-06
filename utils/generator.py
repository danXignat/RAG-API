from llama_index.core.llms import ChatMessage, MessageRole, ChatResponseGen
from typing import AsyncGenerator

from services import Globals

async def generate_stream(id: str, response: ChatResponseGen) -> AsyncGenerator[str, None]:
    """Generate streaming response and allocate message in the global chat store"""
    
    message = ""
    for r in response:
        word = r.delta
        message += word
        yield f"{word}\n"
    
    Globals.add_message(chat_id=id, role="assistant", message=message)
    
async def generator(response) -> AsyncGenerator[str, None]:
    for r in response:
        yield f"{r}\n"
    
    