import os
os.environ["HF_HUB_OFFLINE"] = "1"


import logging
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from .core.config import settings
from .api.v1 import router as v1_router
from .services.translator import TranslatorService, translation_service
from .grpc.server import serve_grpc

# logger setup
logger = logging.getLogger("translator")
logging.basicConfig(level=logging.INFO)

grpc_server = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Loading translation model...")
    global translation_service
    translation_service = TranslatorService(model_name="Helsinki-NLP/opus-mt-uk-pl")

    logger.info("Starting up grpc server...")
    global grpc_server
    grpc_server = serve_grpc()

    yield

    # Shutdown
    logger.info("Shutting down...")
    if grpc_server:
        grpc_server.stop(0)


app = FastAPI(title= settings.app_name, version=settings.version, lifespan=lifespan)
app.include_router(v1_router)

# run server
try:
    uvicorn.run(app, host = settings.host, port= settings.HTTP_PORT)
finally:
    grpc_server.stop(0)
