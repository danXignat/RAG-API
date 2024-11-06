from llama_index.core import (
    ComposableGraph,
    SimpleKeywordTableIndex,
    TreeIndex, 
    load_graph_from_storage,
    StorageContext,
    ListIndex
)
from typing import List, Optional

from llama_index.core.indices.base import BaseIndex

from services import Globals
from utils.rag import index
from models.database import IndexStore

def get_composable_graph(store: IndexStore, document_ids: Optional[List[str]] = None) -> ComposableGraph:
    """Create and/or persist composable graph """
    
    storage_context = StorageContext.from_defaults(
        persist_dir = store.path,
    )
    
    try:
        graph = load_graph_from_storage(storage_context=storage_context)
        
    except:
        document_ids = document_ids if document_ids else [file.id for file in store.files]
        
        indexes = index.load_indexes(index_ids=document_ids, index_store=store)
        
        graph = ComposableGraph.from_indices(
            TreeIndex,
            children_indices=indexes,
            storage_context=storage_context
        )
        
        graph.storage_context.persist(store.path)

    
    return graph
        
