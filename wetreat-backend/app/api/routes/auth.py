from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import EmailStr
from uuid import uuid4, UUID

from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.config import settings
from app.db.session import get_session
from app.models.user import User, UserRole, RoleEnum
from app.schemas.auth import LoginRequest, Token, RegisterUserRequest

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register-admin", response_model=dict)
async def register_admin(req: RegisterUserRequest, session: AsyncSession = Depends(get_session), x_admin_init: str = Header(default="")):
    # Only allowed with initialization token
    if settings.ADMIN_SIGNUP_TOKEN and x_admin_init != settings.ADMIN_SIGNUP_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid admin init token")
    # If token is blank, allow only if no users exist
    if not settings.ADMIN_SIGNUP_TOKEN:
        count = (await session.execute(select(User))).scalars().all()
        if len(count) > 0:
            raise HTTPException(status_code=403, detail="Admin init token required")
    # Create user
    existing = await session.execute(select(User).where(User.email == req.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=req.email, hashed_password=get_password_hash(req.password), full_name=req.full_name)
    session.add(user)
    await session.flush()
    session.add(UserRole(user_id=user.id, role=RoleEnum.ADMIN))
    await session.commit()
    return {"status": "ok", "user_id": str(user.id)}

@router.post("/register", response_model=dict)
async def register(req: RegisterUserRequest, session: AsyncSession = Depends(get_session), admin=Depends(lambda: None)):
    # For simplicity in this starter, restrict /register to admins via header token (not best practice, better to use require_admin + JWT).
    # In production, expose this in /admin/users with proper auth; here we keep both options.
    raise HTTPException(status_code=405, detail="Use /admin/users to create users")

@router.post("/login", response_model=Token)
async def login(req: LoginRequest, session: AsyncSession = Depends(get_session)):
    q = await session.execute(select(User).where(User.email == req.email))
    user = q.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token(str(user.id))
    return Token(access_token=token)
