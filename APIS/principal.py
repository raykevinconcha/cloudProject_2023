# principal.py
from fastapi import FastAPI, Depends, HTTPException
from crud import create_slices, get_slices, update_slices, delete_slices, create_logs, get_systemsresources, get_nodes, create_vm_images, create_token
from models import SlicesCreate, Slices, LogsCreate, Logs, SystemsResources, NodesCreate, Nodes, VMImagesCreate, VMImages, TokenCreate, Token
from typing import List
from database import Database

app = FastAPI()

def get_db():
    db = Database()
    try:
        yield db
    finally:
        db.close()

# Rutas CRUD para Slices
@app.post("/slices/", response_model=Slices)
async def create_slices_route(slices: SlicesCreate, db: Database = Depends(get_db)):
    return create_slices(db, slices)

@app.get("/slices/", response_model=List[Slices])
async def list_slices(db: Database = Depends(get_db)):
    return get_slices(db)

@app.put("/slices/{slices_id}", response_model=Slices)
async def edit_slices(slices_id: int, slices: SlicesCreate, db: Database = Depends(get_db)):
    existing_slices = get_slices(db)
    if not existing_slices:
        raise HTTPException(status_code=404, detail="Slices not found")
    return update_slices(db, slices_id, slices)

@app.delete("/slices/{slices_id}", response_model=int)
async def delete_slices_route(slices_id: int, db: Database = Depends(get_db)):
    existing_slices = get_slices(db)
    if not existing_slices:
        raise HTTPException(status_code=404, detail="Slices not found")
    return delete_slices(db, slices_id)

# Rutas CRUD para Logs
@app.post("/logs/", response_model=Logs)
async def create_logs_route(logs: LogsCreate, db: Database = Depends(get_db)):
    return create_logs(db, logs)

# Rutas para obtener información
@app.get("/systemsresources/", response_model=List[SystemsResources])
async def list_systemsresources(db: Database = Depends(get_db)):
    return get_systemsresources(db)

@app.get("/nodes/", response_model=List[Nodes])
async def list_nodes(db: Database = Depends(get_db)):
    return get_nodes(db)

# Rutas CRUD para VMImages y Token (creación)
@app.post("/vm_images/", response_model=VMImages)
async def create_vm_images_route(vm_images: VMImagesCreate, db: Database = Depends(get_db)):
    return create_vm_images(db, vm_images)

@app.post("/token/", response_model=Token)
async def create_token_route(token: TokenCreate, db: Database = Depends(get_db)):
    return create_token(db, token)

