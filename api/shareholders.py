# shareholders.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.shareholder import Shareholder
from schemas.shareholder import Shareholder as ShareholderSchema
from schemas.shareholder import ShareholderCreate
from api.dependencies import get_current_admin
from crud.shareholder import get_shareholder, create_shareholder as crud_create_shareholder
from fastapi import Query
from core.security import get_password_hash
from models.audit_event import AuditEvent

router = APIRouter()

@router.get("/api/shareholders/", response_model=list[ShareholderSchema] , tags=['shareholders'])
def list_shareholders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_admin)
):
    shareholders = db.query(Shareholder).offset(skip).limit(limit).all()
    result = []
    for sh in shareholders:
        total_shares = sum(issuance.number_of_shares for issuance in sh.issuances)
        sh.total_shares = total_shares   
        result.append(sh)
    return result


@router.post("/api/shareholders/", response_model=ShareholderSchema ,  tags=['shareholders'])
def create_shareholder(
    shareholder_in: ShareholderCreate,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_admin)
):
    user = db.query(User).filter(User.email == shareholder_in.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash("defaultpass123")  
    user = User(email=shareholder_in.email, hashed_password=hashed_password, role="shareholder")
    db.add(user)
    db.commit()
    db.refresh(user)

    shareholder = crud_create_shareholder(db, shareholder_in, user_id=user.id)



    audit_log = AuditEvent(
        action="CREATE_SHAREHOLDER",
        user_id=current_user.id,
        details=f"Created shareholder '{shareholder.name}' with email '{shareholder.email}'"
    )
    db.add(audit_log)
    db.commit()
    
    return shareholder