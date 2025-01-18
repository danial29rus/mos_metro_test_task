from app.business_services import NewsService
from app.clients.metro import NewsClient
from app.db import Session
from app.db.repos import NewsRepo


async def get_news_service() -> NewsService:
    async with Session() as session:
        repo = NewsRepo(session=session)
        client = NewsClient()
        service = NewsService(news_repo=repo, news_client=client)
        return service
