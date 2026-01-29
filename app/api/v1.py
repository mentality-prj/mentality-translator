from fastapi import APIRouter, Request
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
    if not key or key != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    

# -------------------
'''
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Input(BaseModel):
    text: str

@app.post("/translate")
def translate_endpoint(data: Input):
    result = translate(data.text)
    return {"translation": result}

@app.on_event("startup")
def load_model():
    app.state.tokenizer = MarianTokenizer.from_pretrained(model_name)
    app.state.model = MarianMTModel.from_pretrained(model_name)
    # optional warm-up
    app.state.model.generate(**app.state.tokenizer("warmup", return_tensors="pt"))
    '''