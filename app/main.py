import os
os.environ["HF_HUB_OFFLINE"] = "1"


import logging
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .core.config import settings
from .api.v1 import router as v1_router
from .services.translator import TranslatorService

# logger setup
logger = logging.getLogger("translator")
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Loading translation model...")
    app.translator_service = TranslatorService(model_name="Helsinki-NLP/opus-mt-uk-pl")


    yield
    # Shutdown
    logger.info("Shutting down...")


# download ML models
#from huggingface_hub import hf_hub_download, snapshot_download
#snapshot_download(repo_id="Helsinki-NLP/opus-mt-uk-pl")


app = FastAPI(title= settings.app_name, version=settings.version, lifespan=lifespan)
app.include_router(v1_router)
uvicorn.run(app, host = settings.host, port= settings.HTTP_PORT)

## run gRPC server in background, FastAPI in main loop
#grpc_srv = serve_grpc()
#try:
#    uvicorn.run(app, host="0.0.0.0", port=HTTP_PORT)
#finally:
#    grpc_srv.stop(0)


