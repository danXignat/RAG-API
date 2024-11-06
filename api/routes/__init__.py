
from .static_routes import router as static_router
from .chat_routes import router as chat_router
from .rag_routes import router as rag_router
from fastapi import FastAPI

routers = {"static": static_router, "chat": chat_router, "rag": rag_router}

def include_routers(app: FastAPI) -> None:
    for router in routers.values():
        app.include_router(router)

__all__ = ['include_routers']