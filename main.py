from fastapi import FastAPI
from contextlib import asynccontextmanager

from config.settings import HOST, PORT
from api import DataBase
from api.routes import include_routers

@asynccontextmanager
async def lifespan(app: FastAPI):
    include_routers(app)
    DataBase.init_db()
    yield
    
app: FastAPI = FastAPI(lifespan=lifespan)

if __name__ == '__main__':
    import uvicorn 
    uvicorn.run(app="main:app", host=HOST, port=PORT, reload=True)
    