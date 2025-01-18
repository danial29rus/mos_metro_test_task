from app.configs.base import BaseSettings


class CacheSettings(BaseSettings):
    CACHE_HOST_CRON: str
    CACHE_PORT_CRON: int


cache_settings = CacheSettings()
