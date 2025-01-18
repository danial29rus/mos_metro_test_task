from app.transport.deps import get_news_service


async def cron_parse_news(ctx):
    task = await get_news_service()
    await task.fetch_and_save_news()
