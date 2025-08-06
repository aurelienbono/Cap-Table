# schemas/audit_event.py
from pydantic import BaseModel
from datetime import datetime

class AuditEventBase(BaseModel):
    action: str
    details: str

class AuditEventCreate(AuditEventBase):
    user_id: str

class AuditEvent(AuditEventBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True