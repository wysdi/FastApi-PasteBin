from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)

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
