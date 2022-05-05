from fastapi import APIRouter

from api.endpoints import image, monitorcontrol

api_router = APIRouter()

api_router.include_router(monitorcontrol.router, prefix="/control", tags=["control"])
api_router.include_router(image.router, prefix="/image", tags=["image"])
