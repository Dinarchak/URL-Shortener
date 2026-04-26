from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')


class PostgresConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='postgres_')

    db_name: str
    username: str
    password: str
    port: int
    host: str


class KafkaConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='KAFKA_')

    bootstrap_servers: str
    topic: str


class JWTConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='JWT_')

    token: str
    aud: str


class Config(BaseConfig):    
    kafka: KafkaConfig = Field(default_factory=KafkaConfig)
    db: PostgresConfig = Field(default_factory=PostgresConfig)
    jwt: JWTConfig = Field(default_factory=JWTConfig)
    

config = Config()

print(config)