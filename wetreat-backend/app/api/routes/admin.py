from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.api.deps import require_admin
from app.db.session import get_session
from app.models.user import User, UserRole, RoleEnum
from app.models.patient import Patient, Record, RecordDocument
from app.models.assignment_consult import Assignment
from app.schemas.assignment import AssignmentCreate, AssignmentOut
from app.schemas.user import UserOut

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/records", response_model=list[dict])
async def list_records(session: AsyncSession = Depends(get_session), _admin = Depends(require_admin)):
    stmt = select(Record, Patient).join(Patient, Patient.id == Record.patient_id).order_by(Record.created_at.desc())
    res = await session.execute(stmt)
    items = []
    for rec, pat in res.all():
        items.append({
            "record_id": str(rec.id),
            "patient_id": str(pat.id),
            "patient_name": pat.name,
            "dob": pat.dob.isoformat(),
            "email": pat.email,
            "created_at": rec.created_at.isoformat()
        })
    return items

@router.post("/assign", response_model=AssignmentOut)
async def assign_record(payload: AssignmentCreate, session: AsyncSession = Depends(get_session), admin=Depends(require_admin)):
    # Verify record and physician exist
    rec = (await session.execute(select(Record).where(Record.id == payload.record_id))).scalar_one_or_none()
    if not rec:
        raise HTTPException(status_code=404, detail="Record not found")
    phy = (await session.execute(select(User).where(User.id == payload.physician_id))).scalar_one_or_none()
    if not phy:
        raise HTTPException(status_code=404, detail="Physician not found")
    # ensure physician role
    role = (await session.execute(select(UserRole).where(UserRole.user_id == phy.id, UserRole.role == RoleEnum.PHYSICIAN))).scalar_one_or_none()
    if role is None:
        raise HTTPException(status_code=400, detail="User is not a physician")
    from app.models.assignment_consult import Assignment
    a = Assignment(record_id=payload.record_id, physician_id=payload.physician_id, is_blinded=payload.is_blinded, assigned_by=admin.id)
    session.add(a)
    await session.flush()
    await session.commit()
    return a

@router.get("/physicians", response_model=list[UserOut])
async def list_physicians(session: AsyncSession = Depends(get_session), _admin = Depends(require_admin)):
    # users with PHYSICIAN role
    stmt = select(User).join(UserRole, UserRole.user_id == User.id).where(UserRole.role == RoleEnum.PHYSICIAN)
    res = await session.execute(stmt)
    users = res.scalars().all()
    # attach roles names
    out = []
    for u in users:
        out.append(UserOut(id=u.id, email=u.email, full_name=u.full_name, roles=["PHYSICIAN"], is_active=u.is_active))
    return out

@router.post("/users", response_model=dict)
async def create_user(email: str, password: str, full_name: str | None = None, roles: list[str] = ["PHYSICIAN"], session: AsyncSession = Depends(get_session), _admin=Depends(require_admin)):
    # Create a user and assign roles
    from app.core.security import get_password_hash
    existing = (await session.execute(select(User).where(User.email == email))).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    user = User(email=email, hashed_password=get_password_hash(password), full_name=full_name)
    session.add(user)
    await session.flush()
    from app.models.user import RoleEnum, UserRole
    for r in roles:
        if r not in (RoleEnum.ADMIN, RoleEnum.PHYSICIAN):
            continue
        session.add(UserRole(user_id=user.id, role=r))
    await session.commit()
    return {"user_id": str(user.id)}
