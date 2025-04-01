from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    DATABASE_URL: str = "sqlite:///./papers.db"
    MODEL_NAME: str = "gpt-4o"
    
    class Config:
        env_file = ".env"

settings = Settings()