from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from typing import Union
from pydantic import BaseModel


# class Item(BaseModel):
#     name: str
#     description: Union[str, None] = None
#     price: float
#     tax: Union[float, None] = None


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
    return data



