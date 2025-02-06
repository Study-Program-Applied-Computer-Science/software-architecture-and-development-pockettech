from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.shared_group import SharedGroupCreate, SharedGroup
from app.crud.shared_group import create_shared_group, get_shared_groups, delete_shared_group,update_shared_group, get_shared_groups_by_participant_id
from app.db.database import get_db
from uuid import UUID
from app.schemas.shared_group_participants import SharedGroupParticipantsCreate, SharedGroupParticipantsList
from app.crud.shared_group import create_shared_group_participant, get_shared_group_participants_by_group_id, delete_shared_group_participant
from app.crud import shared_group as crud 
from app.schemas.user import UserResponse
from app.crud.shared_group import get_all_users
from typing import List

router = APIRouter()

#create a shared group
@router.post("/shared_groups", response_model=SharedGroup)
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


@router.get("/shared_groups/{participant_id}", response_model=list[SharedGroup])
def get_shared_groups_by_participant_id_route(participant_id: UUID, db: Session = Depends(get_db)):
    shared_groups = get_shared_groups_by_participant_id(db, participant_id)
    if not shared_groups:
        raise HTTPException(status_code=404, detail="No groups found for this participant")
    return shared_groups



#create a shared group participant
@router.post("/", response_model=SharedGroupParticipantsCreate)
def create_shared_group_participant_route(participant: SharedGroupParticipantsCreate, db: Session = Depends(get_db)):
    shared_group_participants=crud.create_shared_group_participant(db, participant)
    return shared_group_participants

#get shared group participants by group id
@router.get("/participants/{group_id}", response_model=SharedGroupParticipantsList)
def get_shared_group_participants_route(group_id: UUID, db: Session = Depends(get_db)):
    shared_group_participants= crud.get_shared_group_participants_by_group_id(db, group_id)
    if not shared_group_participants:
        raise HTTPException(status_code=404, detail="No participants found for this group")
    return shared_group_participants


#delete shared group participant
# @router.delete("/{user_id}/{group_id}")
# def delete_shared_group_participant_route(user_id: UUID, group_id: UUID, db: Session = Depends(get_db)):
#     try:
#         return delete_shared_group_participant(db, user_id, group_id)
#     except Exception as e: 
#         raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id}")
def delete_shared_group_participant_route(id: UUID, db: Session = Depends(get_db)):
    try:
        return delete_shared_group_participant(db, id)
    except Exception as e: 
        raise HTTPException(status_code=400, detail=str(e))



# TODO: use User service to create the below

@router.get("/users", response_model=list[UserResponse])
def get_all_users_route(db: Session = Depends(get_db)):
    return get_all_users(db)