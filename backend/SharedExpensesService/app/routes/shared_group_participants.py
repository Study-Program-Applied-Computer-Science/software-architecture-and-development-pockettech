from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import shared_group_participants as crud
from app.schemas.shared_group_participants import SharedGroupParticipantsCreate, SharedGroupParticipantsList
from app.db.database import get_db
from uuid import UUID

router = APIRouter()

#create a shared group participant
@router.post("/", response_model=SharedGroupParticipantsCreate)
def create_shared_group_participant(participant: SharedGroupParticipantsCreate, db: Session = Depends(get_db)):
    return crud.create_shared_group_participant(db, participant)

#get shared group participants by group id
@router.get("/participants/{group_id}", response_model=SharedGroupParticipantsList)
def get_shared_group_participants(group_id: UUID, db: Session = Depends(get_db)):
    shared_group_participants= crud.get_shared_group_participants_by_group_id(db, group_id)
    if not shared_group_participants:
        raise HTTPException(status_code=404, detail="No participants found for this group")
    return shared_group_participants


#delete shared group participant
@router.delete("/{participant_id}")
def delete_shared_group_participant(participant_id: UUID, db: Session = Depends(get_db)):
    try:
        return crud.delete_shared_group_participant(db, str(participant_id))
    except Exception as e: 
        raise HTTPException(status_code=400, detail=str(e))

