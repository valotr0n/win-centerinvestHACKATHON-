from fastapi.middleware.cors import CORSMiddleware
from app.middleware import RefreshTokenMiddleware
from app.users.router import router as users_router
from app.pages.router import router as pages_router
import app.ml.module.stt  as stt
import app.ml.module.module2  as fz
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from typing import Union
from pydantic import BaseModel
from sqlalchemy import false

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


class Item(BaseModel):
    message: str

@app.post("/api/message/")
async def create_item(request: Request):
    data = await request.json()
    text_content = data.get("text_content", "")
    response = fz.getUserMessage(text_content)
    return JSONResponse(content={"response": response})



@app.post("/api/result_box")
async def result_box(request: Request):
    data = await request.json()
    text_content = data.get("text_content", "")
    response = fz.results_box(text_content)
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


@app.post("/api/voice/stop/")
def stop_record():
    global gen
    gen = None
    start_voice(0)

def start_voice(x):
    global gen
    if x == 1:
        gen = stt.va_listen()
        return gen
    else:
        gen = '1'
        return gen




def record_voice():
    global gen
    if gen:
        return next(gen)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)