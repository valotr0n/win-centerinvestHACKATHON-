from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi.responses import JSONResponse
import module.module as mdl
from typing import Union
from pydantic import BaseModel

from server.module import stt


class Item(BaseModel):
    message: str

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI()
app.mount("/assets", StaticFiles(directory="../assets"), name="assets")

@app.get("/z")
def read_root():
    return{"Hello": "world"}


templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))



@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


@app.post("/api/message/")
async def create_item(request: Request):
    data = await request.json()
    text_content = data.get("text_content", "")
    response = await mdl.chat(text_content)
    return JSONResponse(content={"response": response})




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
# @app.get("/api/voice/recognize/")
# async def recognize_audio():
#     global gen
#     gen = stt.va_listen()
#     result = next(gen)
#     return JSONResponse(content={"result": result})
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)