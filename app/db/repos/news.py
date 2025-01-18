from datetime import datetime

from sqlalchemy import delete, select

from app.db.repos.base import BaseRepo
from app.models import News


class NewsRepo(BaseRepo):
    model_type = News
    order_by = News.pub_date

    async def get_news_by_date_range(
        self, start_date: datetime, end_date: datetime
    ) -> list[News]:
        query = (
            select(self.model_type)
            .filter(self.model_type.pub_date.between(start_date, end_date))
            .order_by(self.model_type.pub_date)
        )

        records = await self.session.execute(query)
        models = records.scalars().all()
        return models

    async def get_latest_news(self):
        query = (
            select(self.model_type)
            .order_by(self.model_type.pub_date.desc())
            .limit(1)
        )
        records = await self.session.execute(query)
        return records.scalars().first()

    async def clear_all(self):
        query = delete(self.model_type)
        await self.session.execute(query)

    async def clear_and_insert_news(self, news_data: list) -> None:
        async with self.session.begin():
            await self.clear_all()

            if news_data:
                await self.bulk_insert(news_data)
