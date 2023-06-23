import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = os.environ["PROJECT_NAME"]


settings = Settings()