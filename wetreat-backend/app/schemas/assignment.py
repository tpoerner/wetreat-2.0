from pydantic import BaseModel
from uuid import UUID

class AssignmentCreate(BaseModel):
    record_id: UUID
    physician_id: UUID
    is_blinded: bool = True

class AssignmentOut(BaseModel):
    id: UUID
    record_id: UUID
    physician_id: UUID
    is_blinded: bool

    class Config:
        from_attributes = True
