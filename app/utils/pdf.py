from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from io import BytesIO
from datetime import date
from math import floor

def _age_years(dob):
    today = date.today()
    return int((today - dob).days // 365.25)

def build_consultation_pdf(assignment, consultation, record, patient, documents):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4
    y = h - 20*mm

    def line(text, size=11, dy=6*mm):
        nonlocal y
        c.setFont("Helvetica", size)
        c.drawString(20*mm, y, text)
        y -= dy

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(20*mm, y, "WeTreat Consultation Report")
    y -= 10*mm

    # IDs and timestamps
    line(f"Consultation ID: {consultation.id}")
    line(f"Record ID: {record.id}")
    line(f"Created at (record): {record.created_at}")
    line(f"Consultation date: {consultation.consultation_date}")
    y -= 5*mm

    # Patient section (respect blinding)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(20*mm, y, "Patient")
    y -= 7*mm
    if assignment.is_blinded:
        line(f"Patient ID: {patient.id}")
        line(f"Age: {_age_years(patient.dob)} years")
    else:
        line(f"Name: {patient.name}")
        line(f"DOB: {patient.dob}")
        line(f"Email: {patient.email}")
        line(f"Patient ID: {patient.id}")

    y -= 5*mm
    c.setFont("Helvetica-Bold", 13)
    c.drawString(20*mm, y, "Clinical Intake")
    y -= 7*mm
    line(f"Symptoms: {record.symptoms}")
    line(f"Medical history: {record.medical_history}")
    line(f"Current medication: {record.current_medication}")
    if record.patient_notes:
        line(f"Patient notes: {record.patient_notes}")
    y -= 5*mm

    c.setFont("Helvetica-Bold", 13)
    c.drawString(20*mm, y, "Documents")
    y -= 7*mm
    if not documents:
        line("No documents provided.")
    else:
        for d in documents:
            line(f"- {d.label}: {d.url} ({d.description or ''})", size=10, dy=5*mm)

    y -= 5*mm
    c.setFont("Helvetica-Bold", 13)
    c.drawString(20*mm, y, "Consultation")
    y -= 7*mm
    line(f"Type: {consultation.type}")
    line(f"Status: {consultation.status}")
    line(f"Recommendations: {consultation.recommendations}")
    if consultation.physician_notes:
        line(f"Physician notes: {consultation.physician_notes}")

    y -= 10*mm
    c.setFont("Helvetica-Oblique", 10)
    line("This PDF is auto-generated and intended for electronic signature.", size=10)

    c.showPage()
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
