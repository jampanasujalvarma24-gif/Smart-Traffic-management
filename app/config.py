from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Smart Traffic Management"
    database_url: str = "sqlite:///./traffic.db"
    mqtt_enabled: bool = False
    mqtt_broker_url: str = "mqtt://localhost:1883"
    simulation_seed: int = 42
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()

