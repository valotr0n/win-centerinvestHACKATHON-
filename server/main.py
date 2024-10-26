from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi.responses import JSONResponse
import module.module as mdl
from typing import Union
from pydantic import BaseModel



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
    response = await mdl.pidorasiki(text_content)  # Убедитесь, что pidorasiki также асинхронная
    return JSONResponse(content={"response": response})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)