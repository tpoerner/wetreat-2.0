from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
import jwt

from app.core.security import decode_token
from app.db.session import get_session
from app.models.user import User, UserRole, RoleEnum

reuseable_oauth = HTTPBearer(auto_error=False)

async def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(reuseable_oauth), session: AsyncSession = Depends(get_session)) -> User:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    token = credentials.credentials
    try:
        payload = decode_token(token)
        sub = payload.get("sub")
        if not sub:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    stmt = select(User).where(User.id == UUID(sub))
    res = await session.execute(stmt)
    user = res.scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Inactive or not found")
    return user

async def require_admin(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)) -> User:
    stmt = select(UserRole).where(UserRole.user_id == user.id, UserRole.role == RoleEnum.ADMIN)
    res = await session.execute(stmt)
    role = res.scalar_one_or_none()
    if role is None:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user

async def require_physician(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)) -> User:
    stmt = select(UserRole).where(UserRole.user_id == user.id, UserRole.role == RoleEnum.PHYSICIAN)
    res = await session.execute(stmt)
    role = res.scalar_one_or_none()
    if role is None:
        raise HTTPException(status_code=403, detail="Physician privileges required")
    return user
