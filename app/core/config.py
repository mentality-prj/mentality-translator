from pydantic import BaseModel
import os

class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "example-microservice")
    env: str = os.getenv("ENV", "local")
    version: str = os.getenv("VERSION", "0.1.0")
    API_KEY: str = os.getenv("TRANSLATOR_API_KEY", "please-change-me")

    # ML model settings
    MODEL_NAME: str = os.getenv("TRANSLATOR_MODEL", "Helsinki-NLP/opus-mt-uk-pl")

    #gRPC/HTTP settings
    host: str = "127.0.0.1"
    GRPC_HOST: str = "0.0.0.0"
    GRPC_PORT: int = int(os.getenv("GRPC_PORT", 50051))
    HTTP_PORT: int = int(os.getenv("HTTP_PORT", 8001))

    # TLS/mTLS files
    TLS_CERT: str = os.getenv("TLS_CERT", "/certs/server.crt")
    TLS_KEY: str = os.getenv("TLS_KEY", "/certs/server.key")
    TLS_CA: str = os.getenv("TLS_CA", "/certs/ca.crt")  # CA that signed client certs


settings = Settings()