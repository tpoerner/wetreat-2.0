from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ReportOut(BaseModel):
    id: UUID
    consultation_id: UUID
    pdf_path: str | None = None
    generated_at: datetime

    class Config:
        from_attributes = True
