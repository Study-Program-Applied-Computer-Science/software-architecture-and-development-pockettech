from sqlalchemy.orm import Session
from app.models.share_type import ShareType
from app.schemas.share_type import ShareTypeCreate
from uuid import UUID


# def create_share_type(db: Session, share_type: ShareTypeCreate):
#     db_share_type = ShareType(share_type=share_type.share_type)
#     db.add(db_share_type)
#     db.commit()
#     db.refresh(db_share_type)
#     return db_share_type

def get_share_type(db: Session, share_type_id: int):
    return db.query(ShareType).filter(ShareType.id == share_type_id).first()

def get_all_share_types(db: Session):
    return db.query(ShareType).all()
