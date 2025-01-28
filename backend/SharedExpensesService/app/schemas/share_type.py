from pydantic import BaseModel

class ShareTypeBase(BaseModel):
    share_type: str

class ShareTypeCreate(ShareTypeBase):
    pass

class ShareType(ShareTypeBase):
    id: int

    class Config:
        orm_mode = True
