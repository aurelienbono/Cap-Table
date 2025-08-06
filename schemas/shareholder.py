# schemas/shareholder.py
from pydantic import BaseModel
from typing import Optional, List

class ShareholderBase(BaseModel):
    name: str
    email: str

class ShareholderCreate(ShareholderBase):
    pass

class Shareholder(ShareholderBase):
    id: str
    total_shares: Optional[int] = 0

    class Config:
        orm_mode = True