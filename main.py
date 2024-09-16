from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import Any, Dict, List
import uuid

app = FastAPI()

class JSONItem(BaseModel):
    id: str
    data: Dict[str, Any]

db: List[JSONItem] = []

@app.post("/items/", response_model=JSONItem)
def create_item(data: Dict[str, Any] = Body(...)):
    new_item = JSONItem(id=str(uuid.uuid4()), data=data)
    db.append(new_item)
    return new_item

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
