from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Подгружаем .env файл в переменные окружения, без этого не работает Pydantic-Settings
load_dotenv()

# Путь к корню проекта
BASE_DIR = Path(__file__).parent.parent


class Config(BaseSettings):
    JWT_SECRET_KEY: str
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_PASSWORD: str = "password"
    DB_USER: str = "user"
    DB_NAME: str = "todo"

    class ConfigDict:
        env: Path = BASE_DIR / ".env"


config = Config()

DB_URL: str = (
    f"postgresql+asyncpg://"
    f"{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
)
