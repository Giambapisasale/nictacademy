from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
from typing import Any, Dict, List
import uuid
import requests
import uvicorn

app = FastAPI()

SUPABASE_URL = "https://sgutsavjxkymowmpebmk.supabase.co/rest/v1/json_data"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNndXRzYXZqeGt5bW93bXBlYm1rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjY1MDkyMzgsImV4cCI6MjA0MjA4NTIzOH0.b_iTwce4AvE5GZTkP_d3m-mNBlBYxWvzs6s9-8Z6_Ww"

HEADERS = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

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

@app.post("/items/", response_model=JSONItem, summary="Create a new JSON item")
def create_item(data: Dict[str, Any] = Body(..., description="Data to store as JSON")):
    payload = {
        "data": data
    }
    response = requests.post(
        SUPABASE_URL,
        headers={**HEADERS, "Prefer": "return=representation"},
        json=payload
    )
    if response.status_code == 201:
        item = response.json()[0]  # Supabase restituisce una lista
        return JSONItem(**item)
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/items/", response_model=List[JSONItem], summary="Retrieve all JSON items")
def get_items():
    response = requests.get(SUPABASE_URL, headers=HEADERS)
    if response.status_code == 200:
        items = response.json()
        return [JSONItem(**item) for item in items]
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/items/{item_id}", response_model=JSONItem, summary="Retrieve a JSON item by ID")
def get_item(item_id: str):
    params = {"id": f"eq.{item_id}"}
    response = requests.get(SUPABASE_URL, headers=HEADERS, params=params)
    if response.status_code == 200:
        items = response.json()
        if items:
            return JSONItem(**items[0])
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

@app.delete("/items/{item_id}", response_model=dict, summary="Delete a JSON item by ID")
def delete_item(item_id: str):
    params = {"id": f"eq.{item_id}"}
    response = requests.delete(SUPABASE_URL, headers=HEADERS, params=params)
    if response.status_code == 204:
        return {"detail": "Item deleted"}
    elif response.status_code == 404:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)