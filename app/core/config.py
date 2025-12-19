from pydantic import BaseModel
import os

class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "example-microservice")
    env: str = os.getenv("ENV", "local")
    version: str = os.getenv("VERSION", "0.1.0")

settings = Settings()