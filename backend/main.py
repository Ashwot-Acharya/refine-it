from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Users(BaseModel):
    name: str
    password: str
    email: str | None = None


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/items/")
async def create_item(item: Item):
    pass
    