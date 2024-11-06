from fastapi import APIRouter
from fastapi.responses import FileResponse

from models import Creator

router = APIRouter()

@router.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")

@router.get("/")
async def root() -> Creator:
    return Creator()



    
    
    
    