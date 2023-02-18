from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import Paste, PasteIn
from database import SessionLocal, engine

from cruds import crud_create_paste, crud_get_paste, crud_get_pastes
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from typing import List, Optional
router = APIRouter()

responses = {
    404: {"description": "Item not found"},
}


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/paste", response_model=Paste, name="Create new paste")
def create_paste(paste: PasteIn, db: Session = Depends(get_db)):
    result = crud_create_paste(db, paste)
    return result


@router.get("/paste/{paste_id}", response_model=Paste, responses={**responses}, name="Retrieve a single paste")
def get_paste(paste_id: str, db: Session = Depends(get_db)):
    db_paste = crud_get_paste(db, paste_id)
    if db_paste is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Paste not found")
    return db_paste


@router.get("/paste", response_model=List[Paste], responses={**responses},
            name="Retrieve a list of all paste")
def get_pastes(page: int = 1, limit: int = 20, db: Session = Depends(get_db)):
    pastes = crud_get_pastes(db, limit, page)
    return pastes
