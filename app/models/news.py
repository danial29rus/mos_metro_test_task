from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.db import Base


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    pub_date = Column(DateTime, nullable=False, index=True)
    url = Column(String, nullable=False)
    scraped_at = Column(DateTime, nullable=False, default=datetime.utcnow)
