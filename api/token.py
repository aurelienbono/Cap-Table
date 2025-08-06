# token.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from core.security import create_access_token, verify_password , get_password_hash
from schemas.user import UserBase , UserCreate
router = APIRouter()

@router.post("/api/token/",  tags=["token"])
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):

        audit_log = AuditEvent(
            action="LOGIN_FAILED",
            user_id=user.id if user else None,
            details=f"Failed login attempt for email: {form_data.username}"
        )
        db.add(audit_log)
        db.commit()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        

    audit_log = AuditEvent(
        action="LOGIN_SUCCESS",
        user_id=user.id,
        details=f"User '{user.email}' logged in successfully"
    )
    db.add(audit_log)
    db.commit()

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}






@router.post("/api/token/register/", status_code=status.HTTP_201_CREATED,  tags=["token"])
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    if user_in.role != 'admin': 
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Admins only"
        )
    
    hashed_password = get_password_hash(user_in.password)
    new_user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        role=user_in.role,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User successfully registered", "user_id": new_user.id}
