from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import date
from uuid import UUID

from app.api.deps import require_physician, get_current_user
from app.db.session import get_session
from app.models.assignment_consult import Assignment
from app.models.patient import Patient, Record, RecordDocument
from app.schemas.patient import RecordOut, DocumentOut, PatientOut

router = APIRouter(prefix="/physician", tags=["physician"])

def _age_years(dob: date) -> int:
    today = date.today()
    return int((today - dob).days // 365.25)

@router.get("/records", response_model=list[dict])
async def list_assigned_records(session: AsyncSession = Depends(get_session), user=Depends(require_physician)):
    # Join assignments → records → patients
    stmt = (
        select(Assignment, Record, Patient)
        .join(Record, Record.id == Assignment.record_id)
        .join(Patient, Patient.id == Record.patient_id)
        .where(Assignment.physician_id == user.id)
        .order_by(Record.created_at.desc())
    )
    res = await session.execute(stmt)
    items = []
    for a, r, p in res.all():
        item = {
            "record_id": str(r.id),
            "assigned_at": a.created_at.isoformat(),
            "is_blinded": a.is_blinded,
            "created_at": r.created_at.isoformat(),
        }
        if a.is_blinded:
            item |= {"patient_id": str(p.id), "age_years": _age_years(p.dob)}
        else:
            item |= {"patient_id": str(p.id), "name": p.name, "dob": p.dob.isoformat(), "email": p.email}
        items.append(item)
    return items

@router.get("/records/{record_id}", response_model=dict)
async def get_record(record_id: UUID, session: AsyncSession = Depends(get_session), user=Depends(require_physician)):
    # Verify assignment
    a = (await session.execute(select(Assignment).where(Assignment.record_id == record_id, Assignment.physician_id == user.id))).scalar_one_or_none()
    if not a:
        raise HTTPException(status_code=403, detail="Not assigned")
    r = (await session.execute(select(Record).where(Record.id == record_id))).scalar_one_or_none()
    p = (await session.execute(select(Patient).where(Patient.id == r.patient_id))).scalar_one_or_none()
    docs = (await session.execute(select(RecordDocument).where(RecordDocument.record_id == r.id))).scalars().all()
    data = {
        "record": {"id": str(r.id), "symptoms": r.symptoms, "medical_history": r.medical_history, "current_medication": r.current_medication, "patient_notes": r.patient_notes},
        "documents": [{"id": str(d.id), "url": d.url, "label": d.label, "description": d.description} for d in docs],
    }
    if a.is_blinded:
        data["patient"] = {"id": str(p.id), "age_years": _age_years(p.dob)}
    else:
        data["patient"] = {"id": str(p.id), "name": p.name, "dob": p.dob.isoformat(), "email": p.email}
    return data
