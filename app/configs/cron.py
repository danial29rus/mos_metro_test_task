from app.configs.base import BaseSettings


class CronSettings(BaseSettings):

    PARSE_NEWS_HOURS: set[int] = {h for h in range(24)}
    PARSE_NEWS_MINUTES: set[int] = {m for m in range(0, 60, 10)}


cron_settings = CronSettings()
