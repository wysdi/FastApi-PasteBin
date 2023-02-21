from sqlalchemy.orm import Session
import uuid
import secrets
from datetime import datetime, date, timedelta
from .models import Paste
from .schemas import PasteIn


def crud_create_paste(db: Session, paste: PasteIn):

    db_paste = Paste(
        paste_id=str(uuid.uuid4()),
        url=secrets.token_urlsafe(10),
        content=paste.content,
        expired_at=paste.expired_at
    )
    db.add(db_paste)
    db.commit()
    db.refresh(db_paste)
    return db_paste


def crud_get_pastes(db: Session, limit: int = 20, page: int = 1):
    offset = limit * (page - 1)
    query = db.query(Paste)
    return query.offset(offset).limit(limit).all()


def crud_get_paste(db: Session, paste_id: str):
    return db.query(Paste).filter(Paste.paste_id == paste_id).first()


def crud_delete_paste(db: Session, paste_id: str):
    db_delete = crud_get_paste(db, paste_id)
    if db_delete:
        db.delete(db_delete)
        db.commit()
        return True


def crud_update_paste(db: Session, paste_id: str, paste: PasteIn):
    db_paste = crud_get_paste(db, paste_id)
    if db_paste:
        paste_data = paste.dict(exclude_unset=True)
        for key, value in paste_data.items():
            setattr(db_paste, key, value)
        db.add(db_paste)
        db.commit()
        db.refresh(db_paste)
        return db_paste


def crud_paste_public_url(db: Session, paste_url: str):
    db_paste = db.query(Paste).filter(Paste.url == paste_url).first()
    error_text ='Paste not exist'
    if db_paste:
        if not db_paste.is_expired:
            return { "content": db_paste.content}
        error_text = 'Paste is already expired'

    return {"error": error_text }


