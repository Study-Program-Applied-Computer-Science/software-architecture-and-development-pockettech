from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.shared_group import SharedGroup
from app.schemas.shared_group import SharedGroupCreate, SharedGroup
from app.crud import shared_group as shared_group_crud
from uuid import UUID


router = APIRouter()

@router.post("/", response_model=SharedGroup)
def create_shared_group(group: SharedGroupCreate, db: Session = Depends(get_db)):
    try:
        return shared_group_crud.create_shared_group(db, group)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))




@router.get("/", response_model=list[SharedGroup])
def get_shared_groups(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return shared_group_crud.get_shared_groups(db, skip=skip, limit=limit)


@router.get("/{group_id}", response_model=SharedGroup)
def get_shared_group(group_id: UUID, db: Session = Depends(get_db)):
    group = shared_group_crud.get_shared_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    try:
        return SharedGroup.from_orm(group)  # Convert to Pydantic schema
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serializing group: {str(e)}")

@router.put("/{group_id}", response_model=SharedGroup)
def update_shared_group(group_id: UUID, group_data: SharedGroupCreate, db: Session = Depends(get_db)):
    updated_group = shared_group_crud.update_shared_group(db, group_id, group_data)
    if not updated_group:
        raise HTTPException(status_code=404, detail="Group not found")
    return updated_group

@router.delete("/{group_id}", response_model=SharedGroup)
def delete_shared_group(group_id: UUID, db: Session = Depends(get_db)):
    group = shared_group_crud.delete_shared_group(db, group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group
