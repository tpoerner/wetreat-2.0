from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from datetime import date

from app.api.deps import require_physician, require_admin
from app.db.session import get_session
from app.models.assignment_consult import Assignment, Consultation, ConsultationStatus
from app.models.patient import Patient, Record, RecordDocument
from app.schemas.consultation import ConsultationCreate, ConsultationUpdate, ConsultationOut
from app.utils.pdf import build_consultation_pdf

router = APIRouter(prefix="/consultations", tags=["consultations"])

@router.post("", response_model=ConsultationOut)
async def create_consultation(payload: ConsultationCreate, session: AsyncSession = Depends(get_session), user=Depends(require_physician)):
    # Ensure physician is assigned to record
    a = (await session.execute(select(Assignment).where(Assignment.record_id == payload.record_id, Assignment.physician_id == user.id))).scalar_one_or_none()
    if not a:
        raise HTTPException(status_code=403, detail="Not assigned to this record")
    c = Consultation(record_id=payload.record_id, physician_id=user.id, type=payload.type, consultation_date=payload.consultation_date, recommendations=payload.recommendations, physician_notes=payload.physician_notes, status=ConsultationStatus.DRAFT)
    session.add(c)
    await session.flush()
    await session.commit()
    return c

@router.patch("/{consultation_id}", response_model=ConsultationOut)
async def update_consultation(consultation_id: UUID, payload: ConsultationUpdate, session: AsyncSession = Depends(get_session), user=Depends(require_physician)):
    c = (await session.execute(select(Consultation).where(Consultation.id == consultation_id, Consultation.physician_id == user.id))).scalar_one_or_none()
    if not c:
        raise HTTPException(status_code=404, detail="Consultation not found")
    if c.status == ConsultationStatus.CLOSED:
        raise HTTPException(status_code=400, detail="Consultation is closed")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(c, field, value)
    await session.commit()
    await session.refresh(c)
    return c

@router.post("/{consultation_id}/close", response_model=ConsultationOut)
async def close_consultation(consultation_id: UUID, session: AsyncSession = Depends(get_session), user=Depends(require_physician)):
    c = (await session.execute(select(Consultation).where(Consultation.id == consultation_id, Consultation.physician_id == user.id))).scalar_one_or_none()
    if not c:
        raise HTTPException(status_code=404, detail="Consultation not found")
    c.status = ConsultationStatus.CLOSED
    await session.commit()
    await session.refresh(c)
    return c

@router.get("/{consultation_id}/report", response_class=Response)
async def generate_report(consultation_id: UUID, session: AsyncSession = Depends(get_session), user=Depends(require_physician)):
    # Load consultation + record + patient + docs
    c = (await session.execute(select(Consultation).where(Consultation.id == consultation_id, Consultation.physician_id == user.id))).scalar_one_or_none()
    if not c:
        raise HTTPException(status_code=404, detail="Consultation not found")
    r = (await session.execute(select(Record).where(Record.id == c.record_id))).scalar_one_or_none()
    a = (await session.execute(select(Assignment).where(Assignment.record_id == r.id, Assignment.physician_id == user.id))).scalar_one_or_none()
    p = (await session.execute(select(Patient).where(Patient.id == r.patient_id))).scalar_one_or_none()
    docs = (await session.execute(select(RecordDocument).where(RecordDocument.record_id == r.id))).scalars().all()

    if c.status != "CLOSED":
        # You can allow draft/submitted to preview; here we restrict to CLOSED to match spec
        raise HTTPException(status_code=400, detail="Close consultation before generating report")

    pdf_bytes = build_consultation_pdf(assignment=a, consultation=c, record=r, patient=p, documents=docs)
    return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=consultation_{consultation_id}.pdf"})
