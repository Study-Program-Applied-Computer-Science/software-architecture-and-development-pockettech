from uuid import uuid4, UUID
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session
from app.models.shared_group import SharedGroup
from app.schemas.shared_group import SharedGroupCreate
from app.models.shared_group_participants import SharedGroupParticipants
from app.schemas.shared_group_participants import SharedGroupParticipantsCreate
from app.models.user import User as User

# create a shared group
def create_shared_group(db: Session, group: SharedGroupCreate):
    db_group = SharedGroup(  
        group_name=group.group_name
    )
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    db_group_participant = create_shared_group_participant(db, participant=SharedGroupParticipants(
        group_id=db_group.id,
        participant_user_id=group.user_id
     ))
    db.add(db_group_participant)
    db.commit()
    db.refresh(db_group_participant)
    #return db_group
    return {"id": db_group.id, "group_name": db_group.group_name}

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


# get groups shared with a participant id
def get_shared_groups_by_participant_id(db: Session, participant_id: UUID):
    return db.query(SharedGroup
    ).join(SharedGroupParticipants
    ).filter(SharedGroupParticipants.participant_user_id == participant_id
    ).all()

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
# def delete_shared_group_participant(db: Session, user_id: UUID, group_id: UUID):
#     db_participant = db.query(SharedGroupParticipants
#     ).filter(
#         and_(
#             SharedGroupParticipants.participant_user_id == user_id, 
#             SharedGroupParticipants.group_id==group_id
#             )
#             ).first()
#     if db_participant is None:
#         return None
#     db.delete(db_participant)
#     db.commit()
#     return db_participant

def delete_shared_group_participant(db: Session, id: UUID):
    db_participant = db.query(SharedGroupParticipants
    ).filter(SharedGroupParticipants.id == id).first()
    if db_participant is None:
        return None
    db.delete(db_participant)
    db.commit()
    return db_participant


# Get shared group participants by group id
# TODO: use user service instead of joining user table
def get_shared_group_participants_by_group_id(db: Session, group_id: UUID):
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

#def get all users
# TODO: use User service to create the below
def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()

