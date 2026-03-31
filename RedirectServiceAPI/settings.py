from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    get_url_by_slug_path: str
    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_TOPIC: str

config = Config()
                                      