from sqlalchemy.orm import Session
from app.models.shared_group import SharedGroup
from app.schemas.shared_group import SharedGroupCreate
from uuid import UUID
from sqlalchemy.exc import IntegrityError

def create_shared_group(db: Session, group: SharedGroupCreate):
    db_group = SharedGroup(**group.dict())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

#def get_shared_group(db: Session, group_id: str):
 #   return db.query(SharedGroup).filter(SharedGroup.id == group_id).first()

def get_shared_group(db: Session, group_id: UUID):
    try:
        group = db.query(SharedGroup).filter(SharedGroup.id == group_id).first()
        print(f"Retrieved group: {group}")  # Debug log
        return group
    except Exception as e:
        print(f"Error while fetching group: {str(e)}")  # Debug error log
        return None



def get_shared_groups(db: Session, skip: int = 0, limit: int = 10):
    return db.query(SharedGroup).offset(skip).limit(limit).all()


def update_shared_group(db: Session, group_id: UUID, updated_data: SharedGroupCreate):
    group = db.query(SharedGroup).filter(SharedGroup.id == group_id).first()
    if not group:
        return None
    for key, value in updated_data.dict().items():
        setattr(group, key, value)
    db.commit()
    db.refresh(group)
    return group

def delete_shared_group(db: Session, group_id: UUID):
    group = db.query(SharedGroup).filter(SharedGroup.id == group_id).first()
    if not group:
        return None
    db.delete(group)
    db.commit()
    return group



