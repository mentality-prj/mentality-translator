from fastapi import APIRouter
from ..core.config import settings

router = APIRouter(prefix="/v1")

@router.get("/health")
def health():
    return {"status": "ok", "service": settings.app_name, "version": settings.version}

@router.get("/hello")
def hello(name: str = "world"):
    return {"message": f"Hello, {name}!"}