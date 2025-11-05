from pydantic_settings import BaseSettings


class EnvSettings(
    BaseSettings,
    env_file=".env",
):
    postgres_dsn: str

def get_env_settings() -> EnvSettings:
    return EnvSettings()