# crud/audit_event.py
from sqlalchemy.orm import Session
from models.audit_event import AuditEvent

def log_audit_event(db: Session, action: str, user_id: str, details: str):
    audit_event = AuditEvent(
        action=action,
        user_id=user_id,
        details=details
    )
    db.add(audit_event)
    db.commit()
