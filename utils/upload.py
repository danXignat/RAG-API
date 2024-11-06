from fastapi import UploadFile, File
from sqlmodel import Session, select
from typing import List, Any
import shutil

from models import Added
from models.database import MetaData, IndexStore
from models.schema import AddedFile
from .hashing import generate_file_id

def save_to_db(data: Any, session: Session):
    """Save object of any type to database and return the updated object"""
    session.add(data)
    session.commit()
    session.refresh(data)
    
    return data
        
def is_stored(session: Session, metadata_id: str, index_store_id: str) -> bool:
    statement = (
        select(MetaData)
        .where(MetaData.index_store_id == index_store_id)
        .where(MetaData.id == metadata_id)
    )
    
    result = session.exec(statement).first()
    
    return result is not None
    
def store_documents(session: Session, store_id: str, files: List[UploadFile] = File(...)) -> List[AddedFile]:
    added_files = []
    
    for file in files:
        data = MetaData(
            id=generate_file_id(file.file),
            name=file.filename
        )

        if is_stored(session, data.id, store_id):
            added_files.append(
                AddedFile(is_added=Added.REPLICA, data=data)
            )
            continue
        
        with open(data.path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        added_files.append(
            AddedFile(is_added=Added.SUCCESS, data=data)
        )
    
    return added_files