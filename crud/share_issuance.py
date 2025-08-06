# crud/share_issuance.py
from sqlalchemy.orm import Session
from models.share_issuance import ShareIssuance
from schemas.share_issuance import ShareIssuanceCreate

def get_issuance(db: Session, issuance_id: int) -> ShareIssuance:
    return db.query(ShareIssuance).filter(ShareIssuance.id == issuance_id).first()

def get_issuances_by_shareholder(db: Session, shareholder_id: int):
    return db.query(ShareIssuance).filter(ShareIssuance.shareholder_id == shareholder_id).all()

def get_all_issuances(db: Session):
    return db.query(ShareIssuance).all()

def create_share_issuance(db: Session, issuance_in: ShareIssuanceCreate) -> ShareIssuance:
    db_issuance = ShareIssuance(
        shareholder_id=issuance_in.shareholder_id,
        number_of_shares=issuance_in.number_of_shares,
        price=issuance_in.price,
        issued_date=issuance_in.issued_date
    )
    db.add(db_issuance)
    db.commit()
    db.refresh(db_issuance)
    return db_issuance