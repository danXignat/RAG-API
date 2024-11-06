from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
import os

from config.settings import DOCUMENTS_DIR_PATH, DATA_PATH, INDEX_DIR_PATH


class MetaDataBase(SQLModel):
    id: str = Field(..., primary_key=True)
    name: str
    
class MetaData(MetaDataBase, table=True):
    path: Optional[str] = None
    index_path : Optional[str] = None
    extension: Optional[str] = None
    index_store_id : Optional[str] = Field(default= None, foreign_key="indexstore.id")
    index_store: Optional["IndexStore"] = Relationship(back_populates="files")
     
    def __init__(self, name: str, id: str, index_store: Optional["IndexStore"] = None):
        super().__init__(name=name, id=id)
        
        _, self.extension = os.path.splitext(self.name)
        self.path = os.path.join(DOCUMENTS_DIR_PATH, self.id + self.extension)
        self.index_path = os.path.join(INDEX_DIR_PATH, self.id)
        self.index_store = index_store

    def get_downgrade(self) -> MetaDataBase:
        return MetaDataBase(id=self.id, name=self.name)
    
class IndexStore(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str 
    path: Optional[str] = None
    files: List["MetaData"] = Relationship(back_populates="index_store")
    
    def __init__(self, name: str, id: str):
        self.name=name
        self.id=id        
        self.path = os.path.join(DATA_PATH, self.name) + '/'