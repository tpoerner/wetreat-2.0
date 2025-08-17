from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Date, DateTime, ForeignKey, func, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base

class Patient(Base):
    __tablename__ = "patients"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255))
    dob: Mapped[Date] = mapped_column(Date)
    email: Mapped[str] = mapped_column(String(255))
    created_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())

    records: Mapped[list["Record"]] = relationship("Record", back_populates="patient", cascade="all, delete-orphan")

class Record(Base):
    __tablename__ = "records"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"), index=True)
    symptoms: Mapped[str] = mapped_column(Text)
    medical_history: Mapped[str] = mapped_column(Text)
    current_medication: Mapped[str] = mapped_column(Text)
    patient_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())

    patient: Mapped["Patient"] = relationship("Patient", back_populates="records")
    documents: Mapped[list["RecordDocument"]] = relationship("RecordDocument", back_populates="record", cascade="all, delete-orphan")
    assignments: Mapped[list["Assignment"]] = relationship("Assignment", back_populates="record", cascade="all, delete-orphan")
    consultations: Mapped[list["Consultation"]] = relationship("Consultation", back_populates="record", cascade="all, delete-orphan")

class RecordDocument(Base):
    __tablename__ = "record_documents"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    record_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("records.id", ondelete="CASCADE"), index=True)
    url: Mapped[str] = mapped_column(String(1024))
    label: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    created_at: Mapped = mapped_column(DateTime(timezone=True), server_default=func.now())

    record: Mapped["Record"] = relationship("Record", back_populates="documents")
