from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.orm import Session

from . import curd, models, schemas
# from . import curd
# import models
# import schemas

from . database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


# Dependency
# def get_db():
#   db = SessionLocal()
#   try:
#     yield db
#   finally:
#     db.close()

def get_db(request: Request):
    return request.state.db

@app.post('/users', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
  db_user = curd.get_user_by_email(db, email=user.email)
  if db_user:
    raise HTTPException(status_code=400, detail='Email already registered')
  return curd.create_user(db=db, user=user)


@app.get('/users/', response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  users = curd.get_users(db, skip=skip, limit=limit)
  return users

@app.get('/users/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
  db_user = curd.get_user(db, user_id=user_id)
  if db_user is None:
    raise HTTPException(status_code=400, detail='User not found')
  return db_user

@app.get('/users/{user_id}/item', response_model=schemas.Item)
def create_item_for_user(user_id: int, item: schemas.Item, db: Session = Depends(get_db)):
  return curd.create_user_item(db, item=item, user_id=user_id)


@app.get('/items/', response_model=schemas.Item)
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  items = curd.get_items(db, skip=skip, limit=limit)
  return items