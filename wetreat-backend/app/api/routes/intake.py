from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.models.patient import Patient, Record, RecordDocument
from app.schemas.patient import PatientIn, RecordIn, DocumentIn
from sqlalchemy import select
import uuid

router = APIRouter(prefix="/intake", tags=["intake"])

@router.post("", response_model=dict)
async def create_intake(patient: PatientIn, record: RecordIn, documents: list[DocumentIn] | None = None, session: AsyncSession = Depends(get_session)):
    # Create Patient
    p = Patient(name=patient.name, dob=patient.dob, email=patient.email)
    session.add(p)
    await session.flush()
    # Create Record
    r = Record(patient_id=p.id, symptoms=record.symptoms, medical_history=record.medical_history,
               current_medication=record.current_medication, patient_notes=record.patient_notes)
    session.add(r)
    await session.flush()
    # Documents
    if documents:
        for d in documents:
            session.add(RecordDocument(record_id=r.id, url=d.url, label=d.label, description=d.description))
    await session.commit()
    return {"patient_id": str(p.id), "record_id": str(r.id)}
