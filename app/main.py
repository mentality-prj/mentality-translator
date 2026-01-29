import logging
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .core.config import settings
from .api.v1 import router as v1_router
from .services.translator import translator_service


#from app.services.translator_service import serve_grpc


# logger setup
logger = logging.getLogger("translator")
logging.basicConfig(level=logging.INFO)

# Load translator pipeline once
#logger.info(f"Loading model {MODEL_NAME}...")
#translator_pipe = pipeline("translation", MODEL_NAME)
#logger.info("Model loaded.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Loading translation model...")
    # translator_pipe = pipeline("translation", MODEL_NAME)


    yield
    # Shutdown
    logger.info("Shutting down...")


app = FastAPI(title= settings.app_name, version=settings.version, lifespan=lifespan)
app.include_router(v1_router)


uvicorn.run(app, host = settings.host, port= settings.HTTP_PORT)


## run gRPC server in background, FastAPI in main loop
#grpc_srv = serve_grpc()
#try:
#    uvicorn.run(app, host="0.0.0.0", port=HTTP_PORT)
#finally:
#    grpc_srv.stop(0)


import logging
import uvicorn

from fastapi import FastAPI
from .core.config import settings
from .api.v1 import router as v1_router

logger = logging.getLogger("translator")
logging.basicConfig(level=logging.INFO)


app = FastAPI(
    title="Translation Microservice",
    version="0.1.0",
    lifespan=lifespan
)
app.include_router(v1_router)

uvicorn.run(app, host=settings.host, port=settings.HTTP_PORT)