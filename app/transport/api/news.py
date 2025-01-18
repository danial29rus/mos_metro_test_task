from fastapi import APIRouter, Depends

from app.business_services import NewsService
from app.schemas import NewsItem
from app.transport.deps import get_news_service

router = APIRouter()


@router.get("/metro/news")
async def get_news(
    day: int = 5, news_service: NewsService = Depends(get_news_service)
) -> list[NewsItem]:
    news = await news_service.get_news_for_last_n_days(days=day)
    return news
