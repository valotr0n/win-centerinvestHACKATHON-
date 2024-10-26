from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.middleware import RefreshTokenMiddleware
from app.users.router import router as users_router
from app.pages.router import router as pages_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from app.ml.module.module import chat
import app.ml.module.stt  as stt
import app.ml.module.fuzzwuzz  as fz
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi.responses import JSONResponse
from typing import Union
from pydantic import BaseModel

app = FastAPI()

app.include_router(users_router)
app.include_router(pages_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

origins = ["*"]

app.add_middleware(RefreshTokenMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type", "Authorization", "Set-Cookie", "Access-Control-Allow-Origin", "Access-Control-Allow-Headers"],
)

@app.post("/api/message")
async def create_item(request: Request):
    data = await request.json()
    text_content = data.get("text_content", "")
    response = await chat(text_content)  # Убедитесь, что pidorasiki также асинхронная
    return JSONResponse(content={"response": response})




    
# ГОЛОС
gen = None  # Глобальная переменная для хранения генератора

@app.get("/api/voice/start_voice/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    start_voice(item_id)
    return {"item_id": item_id, "q": q}

@app.get("/api/voice/recognize/")
async def recognize_audio():
    global gen  # Используем глобальную переменную
    try:
        if gen is None:
            gen = stt.va_listen()  # Инициализация генератора, если он не был инициализирован
        result = next(gen)
        return JSONResponse(content={"result": result})
    except StopIteration:
        return JSONResponse(content={"result": "No more data"}, status_code=404)

def start_voice(x):
    global gen
    if x == 1:
        gen = stt.va_listen()
        return gen
    else:
        gen = '1'
        return gen

def record_voice():
    global gen  # Используем глобальную переменную
    return next(gen)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)