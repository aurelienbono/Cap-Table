# audit.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.audit_event import AuditEvent
from api.dependencies import get_current_admin

router = APIRouter()

@router.get("/api/audit/" ,  tags=['audit'])
def list_audit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
    limit: int = 100
):
    logs = db.query(AuditEvent).order_by(AuditEvent.created_at.desc()).limit(limit).all()
    return [
        {
            "id": log.id,
            "action": log.action,
            "user_email": db.query(User).get(log.user_id).email,
            "details": log.details,
            "created_at": log.created_at.isoformat()
        }
        for log in logs
    ]