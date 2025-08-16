from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, func, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base

class Report(Base):
    __tablename__ = "reports"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    consultation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("consultations.id", ondelete="CASCADE"), unique=True, index=True)
    pdf_path: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    generated_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())
