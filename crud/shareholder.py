from sqlalchemy.orm import Session
from models.shareholder import Shareholder as ShareholderModel
from schemas.shareholder import ShareholderCreate

def get_shareholder(db: Session, shareholder_id: int):
    return db.query(ShareholderModel).filter(ShareholderModel.id == shareholder_id).first()

def create_shareholder(db: Session, shareholder: ShareholderCreate, user_id: int):
    db_shareholder = ShareholderModel(**shareholder.dict(), user_id=user_id)
    db.add(db_shareholder)
    db.commit()
    db.refresh(db_shareholder)
    return db_shareholder