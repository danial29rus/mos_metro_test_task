from datetime import datetime, timedelta

from app.clients.metro import NewsClient
from app.db.repos.news import NewsRepo
from app.models import News
from app.schemas import NewsItem


class NewsService:
    def __init__(self, news_repo: NewsRepo, news_client: NewsClient):
        self.news_repo = news_repo
        self.news_client = news_client

    async def get_news_for_last_n_days(self, days: int) -> list[NewsItem]:
        latest_news = await self.news_repo.get_latest_news()

        if latest_news:
            start_date = latest_news.pub_date - timedelta(days=days)
            end_date = latest_news.pub_date

            news_data = await self.news_repo.get_news_by_date_range(
                start_date, end_date
            )
            return [
                NewsItem(
                    title=news.title,
                    publish_date=news.pub_date,
                    image_url=news.url,
                )
                for news in news_data
            ]
        else:
            return []

    async def get_news_for_period(
        self, start_date: datetime, end_date: datetime
    ) -> list[News]:
        result = await self.news_repo.get_news_by_date_range(
            start_date=start_date, end_date=end_date
        )
        return result

    async def fetch_and_save_news(self):
        try:
            parsed_news = await self.news_client.fetch_news()

            news_data = []
            for item in parsed_news:
                news_data.append(
                    {
                        "title": item.title,
                        "pub_date": item.publish_date,
                        "url": item.image_url,
                    }
                )

            if news_data:
                await self.news_repo.clear_and_insert_news(news_data)
        except Exception as e:
            raise e
