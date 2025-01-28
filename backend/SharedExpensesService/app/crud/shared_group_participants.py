from sqlalchemy.orm import Session
from app.models.shared_group_participants import SharedGroupParticipants
from app.schemas.shared_group_participants import SharedGroupParticipantsCreate
from uuid import UUID


def create_shared_group_participant(db: Session, participant: SharedGroupParticipantsCreate):
    db_participant = SharedGroupParticipants(**participant.dict())
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)
    return db_participant

def get_shared_group_participants(db: Session, group_id: UUID):
    return db.query(SharedGroupParticipants).filter(SharedGroupParticipants.group_id == group_id).all()

def get_participant_by_id(db: Session, participant_id: UUID):
    return db.query(SharedGroupParticipants).filter(SharedGroupParticipants.id == participant_id).first()

def delete_shared_group_participant(db: Session, participant_id: UUID):
    participant = db.query(SharedGroupParticipants).filter(SharedGroupParticipants.id == participant_id).first()
    if not participant:
        return None
    db.delete(participant)
    db.commit()
    return participant


def update_shared_group_participant(db: Session, participant_id: UUID, updated_data: SharedGroupParticipantsCreate):
    participant = db.query(SharedGroupParticipants).filter(SharedGroupParticipants.id == participant_id).first()
    if not participant:
        return None
    for key, value in updated_data.dict().items():
        setattr(participant, key, value)
    db.commit()
    db.refresh(participant)
    return participant
