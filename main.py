from typing import Union
from fastapi import FastAPI, HTTPException

app = FastAPI()

db = {}
"""
Create
Read
Update
Delete
"""

@app.post("/items/{item_id}")
def create_item(item_id: int, text: str = ""):
    db[item_id] = text
    return {"item": "creado"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    item = db.get(item_id)
    return {"item": item}

@app.put("/items/{item_id}")
def read_item(item_id: int, new_text: str = ""):
    item = db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="item not found")
    
    db[item_id] = new_text
    return {item_id: db[item_id]}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    item = db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="item not found")
    
    db.remove(item_id)
    return {"item": "borrado"}
