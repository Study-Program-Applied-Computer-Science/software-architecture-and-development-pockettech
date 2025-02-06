from pydantic import BaseModel
from uuid import UUID

class SharedGroupParticipantsBase(BaseModel):
    group_id: UUID
    participant_user_id: UUID

class SharedGroupParticipantsCreate(SharedGroupParticipantsBase):
    pass

class SharedGroupParticipant(SharedGroupParticipantsBase):
    id: UUID
    name: str
    email_id: str
    phone_number: str

    class Config:
        orm_mode = True

class SharedGroupParticipantsList(BaseModel):
    participants: list[SharedGroupParticipant]
    group_name: str
