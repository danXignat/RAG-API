from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_indices_from_storage,
    ComposableGraph
)

from llama_index.core.indices.base import BaseIndex
from sqlmodel import Session
from typing import List, Coroutine
import os
import time

from config.settings import INDEX_DIR_PATH
from services import Globals
from models.database import MetaData, IndexStore
from utils.timer import atimer, timer

@atimer
async def store_index(file: MetaData) :
    print(f"Processing file with id:{file.id} ...")
    
    file_extractor = {".pdf": Globals.PARSER}
    reader = SimpleDirectoryReader(input_files=[file.path], file_extractor=file_extractor)
    documents = await reader.aload_data()
    print("    Parsed!")
    
    index = VectorStoreIndex.from_documents(documents=documents, embed_model = Globals.EMBED_MODEL)
    print("    Indexed!")
    
    index.set_index_id(file.id)#in index store indexed data is going to have same hashed id as the file 
    
    persist_dir = os.path.join(INDEX_DIR_PATH, file.id)
    os.mkdir(persist_dir)
    index.storage_context.persist(persist_dir)
    
    print("Processed", end=' ')
    
@timer
def load_indexes(index_ids: List[str], index_store: IndexStore) -> List[BaseIndex]:
    print(f"Loading indexes with ids:", *index_ids, sep='\n')
        
    index = load_indices_from_storage(
        storage_context=StorageContext.from_defaults(persist_dir=index_store.path),
        index_ids=index_ids,
        embed_model = Globals.EMBED_MODEL
    )
    
    print("Loaded", end=' ')
    return index