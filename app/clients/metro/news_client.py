import re
from datetime import datetime

from bs4 import BeautifulSoup
from httpx import AsyncClient

from app.schemas import NewsItem


class NewsClient:
    METRO_NEWS_BASE_URL = "https://mosday.ru/news"

    def __init__(self):
        self.base_url: str = self.METRO_NEWS_BASE_URL

    async def fetch_news(self) -> list[NewsItem]:
        async with AsyncClient() as client:
            url = f"{self.base_url}/tags.php?metro"
            response = await client.get(url)

            if response.status_code == 200:
                return self._parse_news(response.text)
            return []

    def _parse_news(self, html_content: str) -> list[NewsItem]:
        soup = BeautifulSoup(html_content, "html.parser")
        news_rows: list = soup.find_all("tr")
        news_list: list[NewsItem] = []

        for row in news_rows:
            date_tag, title_tag, img_tag = self._extract_tags(row)

            if date_tag and title_tag and img_tag:
                date_str: str = date_tag.get_text(strip=True)
                title: str = title_tag.get_text(strip=True)
                image_url: str = self._build_full_image_url(
                    self.base_url, img_tag.get("src")
                )

                publish_date: datetime = self._parse_date(date_str)
                if self._validate_title(title):
                    news_list.append(
                        NewsItem(
                            title=title,
                            publish_date=publish_date,
                            image_url=image_url,
                        )
                    )

        return news_list

    @staticmethod
    def _extract_tags(row) -> tuple:
        date_tag = row.find("font", {"size": "2"})
        title_tag = row.find("font", {"size": "3"})
        img_tag = row.find("img")
        return date_tag, title_tag, img_tag

    @staticmethod
    def _build_full_image_url(
        base_url: str, img_path: str | None
    ) -> str | None:
        if img_path and not img_path.startswith("http"):
            return f"{base_url}/{img_path.lstrip('/')}"
        return img_path

    @staticmethod
    def _parse_date(date_str: str) -> str:
        date_match = re.search(
            r"(\d{2}\.\d{2}\.\d{4})", date_str
        )

        if date_match:
            date_part: str = date_match.group(1)

            try:
                return datetime.strptime(date_part, "%d.%m.%Y").strftime("%Y-%m-%d")
            except ValueError:
                return datetime.now().strftime("%Y-%m-%d")

        return datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def _validate_title(title: str) -> bool:
        return len(title) <= 170
