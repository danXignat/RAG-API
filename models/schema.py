from dataclasses import field
from llama_index.core.llms import ChatMessage
from llama_index.core import Document

from pydantic import BaseModel, Field, field_validator
from enum import Enum

from uuid import UUID, uuid4
from typing import List, Any, Dict
import os

from config.settings import DOCUMENTS_DIR_PATH
from models.database import MetaDataBase, MetaData

class Creator(BaseModel):
    creator: str = "dan ignat"
    
class Message(BaseModel):
    message: str
    chat_id: str

class Chat(BaseModel):
    messages: List[ChatMessage]
    chat_id: str
    
class Added(Enum):
    SUCCESS: str = "success"
    REPLICA: str = "replica"
    FAIL: str = "fail"

class AddedFile(BaseModel):
    is_added: Added
    data: MetaDataBase | MetaData
    
    def downgrade(self) -> None:
        if isinstance(self.data, MetaData):
            self.data = self.data.get_downgrade()
            
        return self
           
    def upgrade(self) -> None:
        if isinstance(self.data, MetaDataBase):
            self.data = MetaData(id=self.data.id, name=self.data.name)
            
        return self
    
class StoreName(BaseModel):
    name: str

class SelectedData(BaseModel):
    index_store_id: str
    index_ids: List[str]