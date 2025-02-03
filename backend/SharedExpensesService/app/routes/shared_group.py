from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.shared_group import SharedGroupCreate, SharedGroup
from app.crud.shared_group import create_shared_group, get_shared_groups, delete_shared_group,update_shared_group
from app.db.database import get_db

router = APIRouter()

#create a shared group
@router.post("/shared_groups/", response_model=SharedGroup)
def create_shared_group_route(
    group: SharedGroupCreate, db: Session = Depends(get_db)
):
    # Call the CRUD function to create the shared group
    db_group = create_shared_group(db=db, group=group)
    return db_group

# Get shared groups
@router.get("/shared_groups/", response_model=list[SharedGroup])
def get_shared_groups_route(db: Session = Depends(get_db)):
    return get_shared_groups(db)

# Delete shared group
@router.delete("/shared_groups/{group_id}")
def delete_shared_group_route(group_id: str, db: Session = Depends(get_db)):
    try:
        return delete_shared_group(db, group_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Update shared group
@router.put("/shared_groups/{group_id}")
def update_shared_group_route(group_id: str, group: SharedGroupCreate, db: Session = Depends(get_db)):
    try:
        return update_shared_group(db, group_id, group)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
