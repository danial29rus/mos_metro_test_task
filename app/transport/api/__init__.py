from fastapi import APIRouter

from app.transport.api import news

router = APIRouter()
router.include_router(news.router, tags=["News"])
