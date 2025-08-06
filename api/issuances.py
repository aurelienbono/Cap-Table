# issuances.py
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.shareholder import Shareholder
from models.share_issuance import ShareIssuance
from schemas.share_issuance import ShareIssuanceCreate, ShareIssuance as IssuanceSchema
from api.dependencies import get_current_user , get_current_admin
from services.pdf_generator import generate_certificate_pdf
from crud.share_issuance import create_share_issuance as crud_create_issuance
from fastapi import Query
from models.audit_event import AuditEvent



router = APIRouter()

@router.get("/api/issuances/", response_model=list[IssuanceSchema] , tags=['issuances'])
def list_issuances(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "admin":
        issuances = db.query(ShareIssuance).all()
    elif current_user.role == "shareholder":
        shareholder = db.query(Shareholder).filter(Shareholder.user_id == current_user.id).first()
        if not shareholder:
            raise HTTPException(status_code=404, detail="Shareholder profile not found")
        issuances = db.query(ShareIssuance).filter(ShareIssuance.shareholder_id == shareholder.id).all()
    else:
        raise HTTPException(status_code=403, detail="Access denied")

    return issuances


@router.post("/api/issuances/", response_model=IssuanceSchema, tags=['issuances'])
def create_issuance(
    issuance_in: ShareIssuanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    shareholder = db.query(Shareholder).filter(Shareholder.id == issuance_in.shareholder_id).first()
    if not shareholder:
        raise HTTPException(status_code=404, detail="Shareholder not found")

    if issuance_in.number_of_shares <= 0:
        raise HTTPException(status_code=400, detail="Number of shares must be positive")

    issuance = crud_create_issuance(db, issuance_in)


    audit_log = AuditEvent(
        action="ISSUE_SHARES",
        user_id=current_user.id,
        details=f"Issued {issuance_in.number_of_shares} shares to shareholder {shareholder.id}"
    )
    db.add(audit_log)
    db.commit()


    print(f"[EMAIL SIMULATION] Sent notification to shareholder {shareholder.email} about {issuance_in.number_of_shares} new shares.")

    return issuance 







@router.get("/api/issuances/{issuance_id}/certificate/", tags=['issuances'])
def get_certificate(
    issuance_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    issuance = db.query(ShareIssuance).filter(ShareIssuance.id == issuance_id).first()
    if not issuance:
        raise HTTPException(status_code=404, detail="Issuance not found")

    if current_user.role == "shareholder":
        shareholder = db.query(Shareholder).filter(Shareholder.user_id == current_user.id).first()
        if not shareholder or shareholder.id != issuance.shareholder_id:
            raise HTTPException(status_code=403, detail="Access denied")

    shareholder = db.query(Shareholder).filter(Shareholder.id == issuance.shareholder_id).first()
    pdf_data = {
        "name": shareholder.name,
        "shares": issuance.number_of_shares,
        "date": issuance.issued_date.strftime("%Y-%m-%d"),
        "issuance_id": issuance.id,
        "price": f"${issuance.price:.2f}" if issuance.price else "N/A"
    }

    pdf_bytes = generate_certificate_pdf(issuance, shareholder.name)

    filename = f"share_certificate_{issuance_id}.pdf"


    audit_log = AuditEvent(
        action="DOWNLOAD_CERTIFICATE",
        user_id=current_user.id,
        details=f"User '{current_user.email}' downloaded certificate for issuance ID: {issuance.id} (Shareholder: {shareholder.name})"
    )
    db.add(audit_log)
    db.commit()

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )