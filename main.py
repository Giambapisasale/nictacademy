from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uuid

app = FastAPI()

class JSONItem(BaseModel):
    id: str
    data: dict

# In-memory storage (puoi sostituire con un database)
db: List[JSONItem] = []

@app.post("/items/", response_model=JSONItem)
def create_item(data: dict):
    item = JSONItem(id=str(uuid.uuid4()), data=data)
    db.append(item)
    return item

@app.get("/items/", response_model=List[JSONItem])
def get_items():
    return db

@app.get("/items/{item_id}", response_model=JSONItem)
def get_item(item_id: str):
    for item in db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}", response_model=dict)
def delete_item(item_id: str):
    global db
    db = [item for item in db if item.id != item_id]
    return {"detail": "Item deleted"}
