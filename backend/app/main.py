from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
import uvicorn
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from starlette.websockets import WebSocket

from app.api import router
from app.config import get_setting
from app.manager import engine

setting = get_setting()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield {"db_engine": engine}

    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(router)

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, token: str = "guest"):
    return templates.TemplateResponse("index.html", {"request": request, "token": token})

@app.get("/admin", response_class=HTMLResponse)
async def read_item(request: Request, token: str = "guest"):
    return templates.TemplateResponse("admin.html", {"request": request, "token": token})

@app.middleware("http")
async def add_ngrok_skip_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["ngrok-skip-browser-warning"] = "true"
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Разрешаем доступ всем устройствам
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=setting.PORT)