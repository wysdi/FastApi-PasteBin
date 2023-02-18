from models import Paste
from sqlalchemy.orm import Session
from schemas import PasteIn
import uuid
import secrets
from datetime import datetime, date, timedelta


def crud_create_paste(db: Session, paste: PasteIn):

    # if expired time not specifield will be expired after 6 hours
    if paste.expired_at is None:
        current = datetime.today()
        paste.expired_at = current + timedelta(hours=6)

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
    db_delete = db.query(Paste).filter(Paste.paste_id == paste_id).first()
    if db_delete:
        db.delete(db_delete)
        db.commit()
        return True




