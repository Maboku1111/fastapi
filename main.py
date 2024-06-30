from fastapi import Depends, FastAPI, HTTPException, Response
from sqlmodel import Session
from contextlib import asynccontextmanager
import models
import database

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This code will be executed when the application starts up
    models.Base.metadata.create_all(bind=database.engine)
    yield
    # This code will be executed when the application shuts down
    database.engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return Response("Server is running")

@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(database.get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.get("/items/")
def read_items(db: Session = Depends(database.get_db)):
    items = db.query(models.Item).all()
    return items

@app.post("/items/")
def create_item(item: models.Item, db: Session = Depends(database.get_db)):
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.put("/items/{item_id}")
def update_item(item_id: int, item: models.Item, db: Session = Depends(database.get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.name = item.name
    db_item.description = item.description
    db_item.price = item.price
    db_item.tax = item.tax
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(database.get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"ok": True}