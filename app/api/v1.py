from fastapi import APIRouter, HTTPException, Request
from ..core.config import settings

router = APIRouter(prefix="/v1")

@router.get("/health")
def health():
    return {"status": "ok", "service": settings.app_name, "version": settings.version}

@router.get("/hello")
def hello(name: str = "world"):
    return {"message": f"Hello, {name}!"}


@router.post("/translate")
async def translate_rest(req: Request):
    body = await req.json()
    key = req.headers.get("authorization")
    if not key:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    if key != f"Bearer {settings.API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid authorization token")
    
    result = translate(data.text)
    return {"translation": result}
    

# -------------------
'''
@app.post("/translate")
def translate_endpoint(data: Input):
    result = translate(data.text)
    return {"translation": result}
    '''