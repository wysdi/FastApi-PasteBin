from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)
from datetime import datetime, date, timedelta

from .database import Base


class Paste(Base):
    __tablename__ = 'pastebin'

    id = Column(Integer, primary_key=True, index=True)
    paste_id = Column(String(50), unique=True, nullable=False)
    url = Column(String(100))
    content = Column(String(16000000))
    expired_at = Column(DateTime)

    def __init__(self, paste_id, url, content, expired_at):
        self.paste_id = paste_id
        self.url = url
        self.content = content
        self.expired_at = expired_at

        # if expired time not specified, it will be expired after 6 hours
        if expired_at is None:
            current = datetime.today()
            self.expired_at = current + timedelta(hours=6)

    @property
    def is_expired(self):
        current = datetime.today()
        return current > self.expired_at