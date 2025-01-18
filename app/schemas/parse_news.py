from datetime import datetime

from pydantic import BaseModel


class NewsItem(BaseModel):
    title: str
    publish_date: datetime
    image_url: str
