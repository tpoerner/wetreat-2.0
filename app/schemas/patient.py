from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import date

class PatientIn(BaseModel):
    name: str
    dob: date
    email: EmailStr

class PatientOut(BaseModel):
    id: UUID
    name: str | None = None
    dob: date | None = None
    age_years: int | None = None
    email: str | None = None

    class Config:
        from_attributes = True

class RecordIn(BaseModel):
    symptoms: str
    medical_history: str
    current_medication: str
    patient_notes: str | None = None

class RecordOut(BaseModel):
    id: UUID
    patient_id: UUID
    symptoms: str
    medical_history: str
    current_medication: str
    patient_notes: str | None = None

    class Config:
        from_attributes = True

class DocumentIn(BaseModel):
    url: str
    label: str
    description: str | None = None

class DocumentOut(BaseModel):
    id: UUID
    url: str
    label: str
    description: str | None = None

    class Config:
        from_attributes = True
