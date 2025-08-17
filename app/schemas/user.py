from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str | None = None
    roles: list[str] = []
    is_active: bool

    class Config:
        from_attributes = True
