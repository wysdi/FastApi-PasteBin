from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from typing import List, Optional
from .schemas import Paste, PasteIn
from .database import SessionLocal, engine
from .cruds import crud_create_paste, crud_get_paste, crud_get_pastes, crud_delete_paste, crud_update_paste, crud_paste_public_url


paste_router = APIRouter()

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

#
@paste_router.post("/paste", response_model=Paste, name="Creating paste")
def create_paste(paste: PasteIn, db: Session = Depends(get_db)):
    result = crud_create_paste(db, paste)
    return result


@paste_router.get("/paste/{paste_id}", response_model=Paste, responses={**responses}, name="Reading paste")
def get_paste(paste_id: str, db: Session = Depends(get_db)):
    db_paste = crud_get_paste(db, paste_id)
    if db_paste is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Paste not found")
    return db_paste


@paste_router.patch("/paste/{paste_id}", response_model=Paste, responses={**responses}, name="Updating paste")
def get_paste(paste_id: str, paste: PasteIn,  db: Session = Depends(get_db)):
    db_paste = crud_update_paste(db, paste_id, paste)
    if db_paste is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Unable to update the paste %s".format(paste_id))
    return db_paste


@paste_router.delete("/paste/{paste_id}", responses={**responses}, name="Deleting paste")
def get_paste(paste_id: str, db: Session = Depends(get_db)):
    deleted_paste = crud_delete_paste(db, paste_id)
    if deleted_paste is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Unable To Delete")
    return {"status": "OK"}


# @paste_router.get("/paste", response_model=List[Paste], responses={**responses},
#             name="Retrieve a list of all paste")
# def get_pastes(page: int = 1, limit: int = 20, db: Session = Depends(get_db)):
#     pastes = crud_get_pastes(db, limit, page)
#     return pastes


@paste_router.get("/{paste_url}", responses={**responses},
            name="published paste (Public Access) at specific time")
def get_posted_paste(paste_url: str,  db: Session = Depends(get_db)):
    paste_content = crud_paste_public_url(db, paste_url)
    if paste_content is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="paste not exists or already expired")
    return paste_content
