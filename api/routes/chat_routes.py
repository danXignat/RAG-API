from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from llama_index.core.llms import ChatMessage
from typing import List

from models import Message, Chat
from services import Globals
from utils import create_chat, generate_stream

router = APIRouter()

@router.get("/chat")
async def get_chats() -> List[Chat]:
    chats = []
    print(len(Globals.CHATS.get_keys()))
    
    for key in Globals.CHATS.get_keys():
        chats.append(
            Chat(messages=Globals.CHATS.get_messages(key), chat_id=key)
        )
        

    return chats

@router.get("/chat/{id}")
async def get_chat(id: str) -> List[ChatMessage]:
    return Globals.CHATS.get_messages(id)

@router.post("/newchat")
async def new_chat() -> str:
    return create_chat()

@router.post("/asking")
async def ask(question: Message) -> StreamingResponse:
    id      = question.chat_id
    Globals.add_message(chat_id=id, role="user", message=question.message)
        
    response = Globals.LLM.stream_chat(
        messages = Globals.CHATS.get_messages(id)
    )
            
    return StreamingResponse(
        content    = generate_stream(id, response), 
        media_type ="text/event-stream"
    )

@router.delete("/chat/delete/{id}")
async def delete_chat(id: str) -> None:
    Globals.CHATS.delete_messages(id)
