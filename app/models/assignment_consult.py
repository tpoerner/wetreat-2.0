from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Date, DateTime, ForeignKey, func, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base

class Assignment(Base):
    __tablename__ = "assignments"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    record_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("records.id", ondelete="CASCADE"), index=True)
    physician_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    is_blinded: Mapped[bool] = mapped_column(Boolean, default=True)
    assigned_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())

    record: Mapped["Record"] = relationship("Record", back_populates="assignments")
    physician: Mapped["User"] = relationship("User", foreign_keys=[physician_id])
    assigned_by_user: Mapped["User"] = relationship("User", foreign_keys=[assigned_by])

class ConsultationType(str):
    PERSONAL = "PERSONAL"
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"
    INPUT_REVIEW = "INPUT_REVIEW"

class ConsultationStatus(str):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    CLOSED = "CLOSED"

from sqlalchemy import Enum as PgEnum

class Consultation(Base):
    __tablename__ = "consultations"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    record_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("records.id", ondelete="CASCADE"), index=True)
    physician_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    type: Mapped[str] = mapped_column(PgEnum(ConsultationType.PERSONAL, ConsultationType.VIDEO, ConsultationType.AUDIO, ConsultationType.INPUT_REVIEW, name="consult_type_enum"))
    consultation_date: Mapped[Date] = mapped_column(Date)
    recommendations: Mapped[str] = mapped_column(Text)
    physician_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(PgEnum(ConsultationStatus.DRAFT, ConsultationStatus.SUBMITTED, ConsultationStatus.CLOSED, name="consult_status_enum"), default=ConsultationStatus.DRAFT)
    created_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    record: Mapped["Record"] = relationship("Record", back_populates="consultations")
