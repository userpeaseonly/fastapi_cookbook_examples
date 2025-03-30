from fastapi import FastAPI, Depends, Request, HTTPException, status
from database import SessionLocal, engine, Item
from client_logging import client_logger
from sqlalchemy.orm import Session
from schemas import ItemSchema

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    client_logger.info(
        f"method: {request.method} "
        f"call: {request.url.path} "
        f"ip: {request.client.host} "
        f"headers: {request.headers} "
        f"query: {request.query_params} "
        f"body: {await request.body()}"
    )
    response = await call_next(request)
    return response

@app.get("/home")
async def read_main():
    return {"message": "Hello World"}


@app.post("/item", response_model=int, status_code=status.HTTP_201_CREATED)
def add_item(item: ItemSchema, db_session: Session = Depends(get_db_session)):
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    return item.id


@app.get("/item/{item_id}", response_model=ItemSchema)  
def get_item(item_id: int, db_session: Session = Depends(get_db_session)):
    if not (item_db := db_session.query(Item).filter(Item.id == item_id).first()):
        raise HTTPException(status_code=404, detail="Item not found")
    return item_db