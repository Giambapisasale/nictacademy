from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
from typing import Any, Dict, List
import uuid

app = FastAPI()

class JSONItem(BaseModel):
    id: str = Field(..., description="Unique identifier for the item")
    data: Dict[str, Any] = Field(..., description="Arbitrary JSON data")

    class Config:
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "data": {
                    "nome": "Esempio",
                    "valore": 123
                }
            }
        }

db: List[JSONItem] = []

@app.post("/items/", response_model=JSONItem, summary="Create a new JSON item")
def create_item(data: Dict[str, Any] = Body(..., description="Data to store as JSON")):
    new_item = JSONItem(id=str(uuid.uuid4()), data=data)
    db.append(new_item)
    return new_item

@app.get("/items/", response_model=List[JSONItem], summary="Retrieve all JSON items")
def get_items():
    return db

@app.get("/items/{item_id}", response_model=JSONItem, summary="Retrieve a JSON item by ID")
def get_item(item_id: str):
    for item in db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}", response_model=dict, summary="Delete a JSON item by ID")
def delete_item(item_id: str):
    global db
    db = [item for item in db if item.id != item_id]
    return {"detail": "Item deleted"}