from fastapi import FastAPI
import jinja2

app = FastAPI()

@app.get("/")
def read_root():
    return{"Hello": "world"}


