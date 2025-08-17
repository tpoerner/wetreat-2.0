from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterUserRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None
    roles: list[str] = []
