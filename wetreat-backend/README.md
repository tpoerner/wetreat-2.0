# WeTreat Backend (FastAPI + SQLAlchemy + JWT)

Backend API for the WeTreat online consultation platform.

## Stack
- FastAPI (async)
- SQLAlchemy 2.0 (async) + Alembic
- PostgreSQL (asyncpg)
- JWT Auth (PyJWT) + passlib[bcrypt]
- ReportLab (PDF generation)
- CORS for Netlify frontend

## Features shipped
- Users with roles (ADMIN, PHYSICIAN). Multiple roles per email supported.
- Public patient intake → creates Patient + Record + Documents
- Admin: list records, create users, assign records to physicians (blind or open)
- Physician: sees only assigned records; blinding enforced server-side
- Consultations: draft/submit/close → lock & generate PDF (non-editable)
- Alembic migration ready

## Quickstart (Local)
1. Python 3.11 recommended
2. `python -m venv .venv && source .venv/bin/activate` (Windows: `.venv\Scripts\activate`)
3. `pip install -r requirements.txt`
4. Set env vars (see `.env.example`) or export them manually.
5. Create DB & run migrations:
   ```bash
   alembic upgrade head
   ```
6. Run API:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Bootstrap first admin
If no admin exists yet, call:
```
POST /auth/register-admin
Header: X-Admin-Init: <ADMIN_SIGNUP_TOKEN>
Body: { "email": "...", "password": "...", "full_name": "..." }
```
Set `ADMIN_SIGNUP_TOKEN` in your environment to a secret string.

### Default URLs
- Docs: `http://localhost:8000/docs`
- Health: `GET /health`

## Deploy on Railway
1. Push this repo to GitHub.
2. On Railway:
   - Create a new **PostgreSQL** database.
   - Create a new **Service** from your repo.
   - Set **Environment Variables**:
     - `DATABASE_URL` (Railway injects automatically when you attach the DB; ensure it begins with `postgresql+asyncpg://`)
     - `JWT_SECRET` (random long string)
     - `ALLOWED_ORIGINS` (comma-separated, e.g. `https://your-netlify-site.netlify.app`)
     - `ADMIN_SIGNUP_TOKEN` (one-time bootstrap token for first admin)
     - `TZ=UTC`
   - Set Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Add a **Volume** if you want to persist generated PDFs on-disk (optional). Otherwise PDFs are generated on-demand.
4. Open a Railway Shell and run Alembic:
   ```bash
   alembic upgrade head
   ```

## Notes
- PDFs are generated with ReportLab and can be streamed/downloaded.
- Blinding: physicians with blinded assignments only see age (years) + patient_id; PHI (name, dob, email) is removed server-side.
- The public `/intake` endpoint is open; consider adding CAPTCHA/rate-limiting in production.
