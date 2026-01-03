from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')


class DatabaseConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix='postgres_')

    db_name: str
    username: str
    password: str
    port: int
    host: str


class AuthConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix='auth_')

    jwt_token: str
    refresh_secret: str
    verification_secret: str


class Config(BaseSettings):
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    auth: AuthConfig = Field(default_factory=AuthConfig)


config = Config()
