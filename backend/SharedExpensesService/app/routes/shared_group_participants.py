from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.crud import shared_group_participants as crud
from app.schemas.shared_group_participants import SharedGroupParticipantsCreate, SharedGroupParticipants
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=SharedGroupParticipants)
def create_shared_group_participant(participant: SharedGroupParticipantsCreate, db: Session = Depends(get_db)):
    return crud.create_shared_group_participant(db, participant)

@router.get("/{group_id}", response_model=list[SharedGroupParticipants])
def get_shared_group_participants(group_id: UUID, db: Session = Depends(get_db)):
    participants = crud.get_shared_group_participants(db, group_id)
    if not participants:
        raise HTTPException(status_code=404, detail="Participants not found")
    return participants

@router.get("/participant/{participant_id}", response_model=SharedGroupParticipants)
def get_participant_by_id(participant_id: UUID, db: Session = Depends(get_db)):
    participant = crud.get_participant_by_id(db, participant_id)
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    return participant

@router.delete("/participant/{participant_id}", response_model=SharedGroupParticipants)
def delete_shared_group_participant(participant_id: UUID, db: Session = Depends(get_db)):
    deleted_participant = crud.delete_shared_group_participant(db, participant_id)
    if not deleted_participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    return deleted_participant


@router.put("/participant/{participant_id}", response_model=SharedGroupParticipants)
def update_shared_group_participant(participant_id: UUID, participant_data: SharedGroupParticipantsCreate, db: Session = Depends(get_db)):
    updated_participant = crud.update_shared_group_participant(db, participant_id, participant_data)
    if not updated_participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    return updated_participant

