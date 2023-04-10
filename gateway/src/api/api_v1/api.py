from fastapi import APIRouter

from src.api.api_v1.endpoints import detect, person


api_router = APIRouter()
api_router.include_router(detect.router, prefix="/detect", tags=["detect"])
api_router.include_router(person.router, prefix="/people", tags=["person"])
