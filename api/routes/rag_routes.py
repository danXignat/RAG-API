from fastapi import APIRouter, File, UploadFile, Depends, Form, HTTPException
from fastapi.responses import StreamingResponse
from sqlmodel import Session, select

from llama_index.core.chat_engine.types import ChatMode

from typing import List, Dict, Generator, AsyncGenerator
from icecream import ic
import os
import uuid

from models.schema import Message, AddedFile, Added, StoreName, SelectedData
from models.database import MetaData, IndexStore
from utils import upload, generator
from services import Globals
from utils.rag import index
from api import DataBase

# import logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/rag/newstore")
async def new_store(
    store_name: StoreName,
    session: Session = Depends(DataBase.get_session)
) -> IndexStore:
    index_store = IndexStore(id=str(uuid.uuid4()), name=store_name.name)
    
    if os.path.exists(index_store.path):
        raise HTTPException(status_code=409, detail="Store name already exists")
    
    os.makedirs(index_store.path)
    
    updated_index_store = upload.save_to_db(
        data   =index_store,
        session=session
    )
    
    return updated_index_store

@router.post("/rag/files/store")
async def store_documents(
    files: List[UploadFile] = File(...),
    store_id: str = Form(...),
    session: Session = Depends(DataBase.get_session)
) -> List[AddedFile]:
    added_files = upload.store_documents(session=session, files=files, store_id=store_id)
        
    success_files = [file.data for file in added_files if file.is_added == Added.SUCCESS]
    
    for file in success_files:
        file.index_store = session.get(IndexStore, store_id)
        
        upload.save_to_db(data=file, session=session)
        
        await index.store_index(file=file)         

    return [
        file.downgrade() for file in added_files
    ]

@router.post("/rag/query")
async def query_question(question: Message) -> str:
    indexes = index.load_index()

    query_engine = indexes.as_query_engine(llm=Globals.LLM)
    
    return str(query_engine.query(question.message))

@router.post("/rag/chat")
async def chat_with_data(
    question: Message,
    selection: SelectedData,
    session: Session = Depends(DataBase.get_session)
) -> StreamingResponse:
    """Chating with selected documents from a selected compartment"""    
    indexes = index.load_index(
        index_ids=selection.index_ids,
        index_store=session.get(IndexStore, selection.index_store_id)
    )    
    
    chat_engine = indexes.as_chat_engine(
        chat_mode=ChatMode.CONDENSE_PLUS_CONTEXT,
        llm=Globals.LLM
    )
    
    response_generator = chat_engine.stream_chat(question.message).response_gen
    
    return StreamingResponse(
        content = generator.generator(response_generator),
        media_type="text/event-stream"
    )
    
@router.get("/rag/files")
async def added_files(session: Session = Depends(DataBase.get_session)) -> List[str]:
    data = session.exec(select(MetaData)).all()
    return [
        doc.name for doc in data
    ]
    