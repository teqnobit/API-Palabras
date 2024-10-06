from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import Palabras, session

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

# Acceso desde cualquier parte gracias al cors
origin = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# API REST
@app.get("/api/{palabra}", tags=["root"])
async def obtener_palabras(palabra: str):
    todo_query = session.query(Palabras).filter(Palabras.palabra_ingles == palabra.capitalize())
    todo = todo_query.first()
    if todo is None:
        raise HTTPException(status_code=404, detail="palabra no encontrada")
    return todo

@app.post("/api/", tags=["root"])
async def introducir_palabras(palabra: str, traduccion: str):
    todo = Palabras(palabra_ingles=palabra.capitalize(), traduccion=traduccion)
    session.add(todo)
    session.commit()
    return {"Palabra agregada": {todo.palabra_ingles : todo.traduccion}}

@app.put("/api/{palabra}", tags=["root"])
async def modificar_palabra(palabra:str, nuevaPalabra: str | None = None, nuevaTraduccion: str | None = None):
    todo_query = session.query(Palabras).filter(Palabras.palabra_ingles == palabra.capitalize())
    todo = todo_query.first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Palabra no encontrada")
    if nuevaPalabra is None and nuevaTraduccion is None:
        raise HTTPException(status_code=200, detail="Ningun cambio realizado")

    if nuevaPalabra and nuevaTraduccion:
        # modificar palabra y traduccion
        todo.palabra_ingles = nuevaPalabra.capitalize()
        todo.traduccion = nuevaTraduccion
    elif nuevaPalabra and nuevaTraduccion is None:
        # modificar palabra pero NO traduccion
        todo.palabra_ingles = nuevaPalabra.capitalize()
    elif nuevaPalabra is None and nuevaTraduccion:
        # modificar traduccion pero NO palabra
        todo.traduccion = nuevaTraduccion

    session.add(todo)
    session.commit()

    if nuevaPalabra:
        todo_query = session.query(Palabras).filter(Palabras.palabra_ingles == nuevaPalabra.capitalize())
    else:
        todo_query = session.query(Palabras).filter(Palabras.palabra_ingles == palabra.capitalize())
    todo = todo_query.first()
    return {"Palabra modificada" : todo}

@app.delete("/api/{palabra}", tags=["root"])
async def eliminar_palabra(palabra:str):
    todo_query = session.query(Palabras).filter(Palabras.palabra_ingles == palabra)
    todo = todo_query.first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Palabra no encontrada")

    session.delete(todo)
    session.commit()
    return {"Palabra eliminada" : palabra}

# db = {}
# """
# Create
# Read
# Update
# Delete
# """

# @app.post("/items/{item_id}")
# def create_item(item_id: int, text: str = ""):
#     db[item_id] = text
#     return {"item": "creado"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int):
#     item = db.get(item_id)
#     return {"item": item}

# @app.put("/items/{item_id}")
# def read_item(item_id: int, new_text: str = ""):
#     item = db.get(item_id)
#     if not item:
#         raise HTTPException(status_code=404, detail="item not found")
    
#     db[item_id] = new_text
#     return {item_id: db[item_id]}

# @app.delete("/items/{item_id}")
# def delete_item(item_id: int):
#     item = db.get(item_id)
#     if not item:
#         raise HTTPException(status_code=404, detail="item not found")
    
#     db.pop(item_id)
#     return {"item": "borrado"}
