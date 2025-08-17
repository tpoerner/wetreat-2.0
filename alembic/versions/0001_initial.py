"""initial tables

Revision ID: 0001_initial
Revises: 
Create Date: 2025-08-16 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    role_enum = sa.Enum('ADMIN', 'PHYSICIAN', name='role_enum')
    consult_type_enum = sa.Enum('PERSONAL', 'VIDEO', 'AUDIO', 'INPUT_REVIEW', name='consult_type_enum')
    consult_status_enum = sa.Enum('DRAFT', 'SUBMITTED', 'CLOSED', name='consult_status_enum')

    role_enum.create(op.get_bind(), checkfirst=True)
    consult_type_enum.create(op.get_bind(), checkfirst=True)
    consult_status_enum.create(op.get_bind(), checkfirst=True)

    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )
    op.create_index('ix_users_email', 'users', ['email'])

    op.create_table('user_roles',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('role', role_enum, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'))
    )
    op.create_unique_constraint('uq_user_role', 'user_roles', ['user_id', 'role'])

    op.create_table('patients',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('dob', sa.Date(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )

    op.create_table('records',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('patient_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('patients.id', ondelete='CASCADE')),
        sa.Column('symptoms', sa.Text(), nullable=False),
        sa.Column('medical_history', sa.Text(), nullable=False),
        sa.Column('current_medication', sa.Text(), nullable=False),
        sa.Column('patient_notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )

    op.create_table('record_documents',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('record_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('records.id', ondelete='CASCADE')),
        sa.Column('url', sa.String(length=1024), nullable=False),
        sa.Column('label', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=1024), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )

    op.create_table('assignments',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('record_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('records.id', ondelete='CASCADE')),
        sa.Column('physician_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('is_blinded', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('assigned_by', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )

    op.create_table('consultations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('record_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('records.id', ondelete='CASCADE')),
        sa.Column('physician_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('type', consult_type_enum, nullable=False),
        sa.Column('consultation_date', sa.Date(), nullable=False),
        sa.Column('recommendations', sa.Text(), nullable=False),
        sa.Column('physician_notes', sa.Text(), nullable=True),
        sa.Column('status', consult_status_enum, nullable=False, server_default=sa.text("'DRAFT'::consult_status_enum")),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )

    op.create_table('reports',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('consultation_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('consultations.id', ondelete='CASCADE'), unique=True),
        sa.Column('pdf_path', sa.String(length=1024), nullable=True),
        sa.Column('generated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
    )

def downgrade() -> None:
    op.drop_table('reports')
    op.drop_table('consultations')
    op.drop_table('assignments')
    op.drop_table('record_documents')
    op.drop_table('records')
    op.drop_table('patients')
    op.drop_table('user_roles')
    op.drop_table('users')
    sa.Enum(name='consult_status_enum').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='consult_type_enum').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='role_enum').drop(op.get_bind(), checkfirst=True)
