from functools import lru_cache
from typing import Literal, Optional

from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=('.env', '.env.local'), extra='ignore')

    app_name: str = Field(default='AgroTrace Prétraitement')
    api_prefix: str = Field(default='/api/v1/pretraitement')

    timescale_host: str = Field(default='timescaledb', alias='TIMESCALE_HOST')
    timescale_port: int = Field(default=5432, alias='TIMESCALE_PORT')
    timescale_user: str = Field(default='postgres', alias='TIMESCALE_USER')
    timescale_password: str = Field(default='postgres123', alias='TIMESCALE_PASSWORD')
    timescale_db: str = Field(default='sensors', alias='TIMESCALE_DB')

    minio_endpoint: str = Field(default='minio:9000', alias='MINIO_ENDPOINT')
    minio_access_key: str = Field(default='minio', alias='MINIO_ACCESS_KEY')
    minio_secret_key: str = Field(default='minio123', alias='MINIO_SECRET_KEY')
    minio_secure: bool = Field(default=False, alias='MINIO_SECURE')
    minio_raw_bucket: str = Field(default='uav-raw', alias='MINIO_RAW_BUCKET')
    minio_tiles_bucket: str = Field(default='uav-tiles', alias='MINIO_TILES_BUCKET')

    kafka_bootstrap_servers: Optional[str] = Field(default=None, alias='KAFKA_BOOTSTRAP_SERVERS')
    kafka_topic_events: str = Field(default='pretraitement.events', alias='KAFKA_PRETRAIT_TOPIC')

    metrics_enabled: bool = Field(default=True, alias='METRICS_ENABLED')
    log_level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR'] = Field(default='INFO', alias='LOG_LEVEL')

    @property
    def sync_database_dsn(self) -> str:
        return (
            f"postgresql+psycopg://{self.timescale_user}:{self.timescale_password}"
            f"@{self.timescale_host}:{self.timescale_port}/{self.timescale_db}"
        )

    @property
    def async_database_dsn(self) -> str:
        return (
            f"postgresql+asyncpg://{self.timescale_user}:{self.timescale_password}"
            f"@{self.timescale_host}:{self.timescale_port}/{self.timescale_db}"
        )

    @property
    def minio_scheme(self) -> str:
        return 'https' if self.minio_secure else 'http'

    @property
    def minio_base_url(self) -> str:
        return f"{self.minio_scheme}://{self.minio_endpoint}"


@lru_cache
def get_settings() -> Settings:
    return Settings()