from sqlalchemy.orm import Session
from app.models.shared_group_participants import SharedGroupParticipants
from app.schemas.shared_group_participants import SharedGroupParticipantsCreate
from uuid import uuid4
from app.models.user import User
from app.models.shared_group import SharedGroup


# create a shared group participant
def create_shared_group_participant(db: Session, participant: SharedGroupParticipantsCreate):
    db_participant = SharedGroupParticipants(
        # id=uuid4(),  
        group_id=participant.group_id,
        participant_user_id=participant.participant_user_id 
    )
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant) 
    return db_participant

# Delete shared group participant
def delete_shared_group_participant(db: Session, participant_id: str):
    db_participant = db.query(SharedGroupParticipants
    ).filter(SharedGroupParticipants.id == participant_id).first()
    if db_participant is None:
        return None
    db.delete(db_participant)
    db.commit()
    return db_participant


# Get shared group participants by group id
# TODO: use user service instead of joining user table
def get_shared_group_participants_by_group_id(db: Session, group_id: str):
    db_query = db.query(
        SharedGroupParticipants.id,
        SharedGroupParticipants.group_id,
        SharedGroupParticipants.participant_user_id,
        User.name,
        User.email_id,
        User.phone_number
    ).join(
        User, 
        SharedGroupParticipants.participant_user_id == User.id
        ).filter(
                SharedGroupParticipants.group_id == group_id
                ).all()
    db_query_group_name = db.query(SharedGroup.group_name).filter(SharedGroup.id == group_id).first()
    db_query_group_name = db_query_group_name[0] if db_query_group_name else None
    participants_list = []
    # participants_list.append(
    #     "group_name": db_query_group_name
    # )
    for participant in db_query:
        participants_list.append({
            "id": participant.id,
            "group_id": participant.group_id,
            "participant_user_id": participant.participant_user_id,
            "name": participant.name,
            "email_id": participant.email_id,
            "phone_number": participant.phone_number
        })
    
    result = {
    "participants": participants_list,
    "group_name": db_query_group_name
    }


    print(result, type(result))

    return result



