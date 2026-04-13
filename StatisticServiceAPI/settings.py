from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')


class DatabaseConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="POSTGRES_")

    db_name: str
    username: str
    password: str
    port: int
    host: str


class KafkaConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="KAFKA_")

    bootstrap_servers: str
    group_id: str
    redirect_topic: str
    creation_topic: str
    


class Config(ConfigBase):
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    kafka: KafkaConfig = Field(default_factory=KafkaConfig)

config = Config()
