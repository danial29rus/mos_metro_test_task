from pydantic_settings import BaseSettings, SettingsConfigDict


class DeploySettings(BaseSettings):

    env_file: str = "deploy/.env"
    model_config = SettingsConfigDict(env_file=env_file, extra="ignore")
