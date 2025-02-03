from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from app.models.shared_group import SharedGroup
from app.schemas.shared_group import SharedGroupCreate



# create a shared group
def create_shared_group(db: Session, group: SharedGroupCreate):
    db_group = SharedGroup(
        id=uuid4(), #not needed  
        group_name=group.group_name
    )
    db.add(db_group)
    db.commit()
    db.refresh(db_group) 
    return db_group

# Get shared groups
def get_shared_groups(db: Session):
    query= db.query(
        SharedGroup.id,
        SharedGroup.group_name
    )

    return query.all()

# delete shared group
def delete_shared_group(db: Session, group_id: UUID):
    db.query(SharedGroup).filter(SharedGroup.id == group_id).delete()
    db.commit()
    return True


# Update shared group
def update_shared_group(db: Session, group_id: UUID, group: SharedGroupCreate):
    db.query(SharedGroup).filter(SharedGroup.id == group_id).update(group.dict())
    db.commit()
    return True