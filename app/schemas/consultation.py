from pydantic import BaseModel
from uuid import UUID
from datetime import date

class ConsultationCreate(BaseModel):
    record_id: UUID
    type: str
    consultation_date: date
    recommendations: str
    physician_notes: str | None = None

class ConsultationUpdate(BaseModel):
    type: str | None = None
    consultation_date: date | None = None
    recommendations: str | None = None
    physician_notes: str | None = None
    status: str | None = None

class ConsultationOut(BaseModel):
    id: UUID
    record_id: UUID
    physician_id: UUID
    type: str
    consultation_date: date
    recommendations: str
    physician_notes: str | None = None
    status: str

    class Config:
        from_attributes = True
