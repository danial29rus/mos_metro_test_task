from arq import cron
from arq.connections import RedisSettings

from app.configs import cache_settings, cron_settings
from app.cron.parse_news import cron_parse_news


class WorkerSettings:
    redis_settings = RedisSettings(
        host=cache_settings.CACHE_HOST_CRON,
        port=cache_settings.CACHE_PORT_CRON,
    )
    cron_jobs = [
        cron(
            cron_parse_news,
            hour=cron_settings.PARSE_NEWS_HOURS,
            minute=cron_settings.PARSE_NEWS_MINUTES,
        )
    ]
