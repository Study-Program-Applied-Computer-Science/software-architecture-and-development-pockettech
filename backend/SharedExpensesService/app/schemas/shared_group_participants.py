from pydantic import BaseModel
from uuid import UUID

class SharedGroupParticipantsBase(BaseModel):
    group_id: UUID
    participant_user_id: UUID

class SharedGroupParticipantsCreate(SharedGroupParticipantsBase):
    pass

class SharedGroupParticipants(SharedGroupParticipantsBase):
    id: UUID

    class Config:
        orm_mode = True
