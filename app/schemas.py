from typing import List, Optional
from datetime import datetime
from pydantic import UUID4, BaseModel


class PasteIn(BaseModel):
    content: str
    expired_at: Optional[datetime] = None


class Paste(PasteIn):

    paste_id: UUID4
    url: str

    class Config:
        orm_mode = True
