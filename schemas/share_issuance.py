# schemas/share_issuance.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ShareIssuanceBase(BaseModel):
    shareholder_id: str
    number_of_shares: int
    price: Optional[float] = None
    issued_date: Optional[datetime] = None

class ShareIssuanceCreate(ShareIssuanceBase):
    pass

class ShareIssuance(ShareIssuanceBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True