from fastapi import APIRouter
from app.api.routes import health, images, users

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
# api_router.include_router(images.router, prefix="/image" ,tags=["image"])
# api_router.include_router(users.router, prefix="/user" ,tags=["user"])
