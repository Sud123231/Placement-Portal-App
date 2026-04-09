# Placement Portal App

Placement Portal App is a full-stack campus recruitment platform with role-based access for Admin, Company, and Student users.

The system supports company onboarding, placement drive lifecycle management, student applications with resume upload, application status tracking, asynchronous CSV export, and scheduled notifications.

## Features

- Role-based authentication using JWT (`Student`, `Company`, `Admin`)
- Student and company registration flows
- Admin moderation:
  - Approve/reject company applications
  - Blacklist companies/students
  - Mark drives completed/cancelled
- Company dashboard:
  - Create drives
  - View applicants for a drive
  - Update application outcomes
- Student dashboard:
  - Browse approved companies
  - View eligible drives (CGPA-filtered)
  - Apply with PDF resume upload
  - View application history and remarks
  - Export application history as CSV (async)
- Background jobs with Celery:
  - Daily reminder emails to students for near-deadline eligible drives
  - Monthly placement activity report email to admin
  - Async CSV generation + export completion notification
- Redis-backed caching with in-memory fallback

## Tech Stack

### Backend

- Flask + Flask-RESTful
- SQLAlchemy + SQLite
- Flask-JWT-Extended
- Redis
- Celery + Celery Beat
- Flask-Mail

### Frontend

- Vue 3
- Vue Router
- Axios
- Vite

## Project Structure

```text
Placement-Portal-App/
|- .gitignore
|- Readme.md
|- Backend/
|  |- app.py
|  |- cache_utils.py
|  |- config.py
|  |- extensions.py
|  |- models.py
|  |- requirements.txt
|  |- tasks.py
|  |- migrations/
|  |- routes/
|  |  |- Application.py
|  |  |- auth.py
|  |  |- company.py
|  |  |- drive.py
|  |  `- student.py
|  `- uploads/
|     |- resumes/
|     `- exports/
`- Frontend/
   |- .gitignore
   |- index.css
   |- index.html
   |- package-lock.json
   |- package.json
   |- README.md
   |- vite.config.js
   |- public/
   `- src/
      |- .gitignore
      |- App.vue
      |- main.js
      |- router/
      |- services/
      `- views/
```

## Prerequisites

- Python 3.10+
- Node.js 18+ (or newer LTS)
- Redis server (local or Docker)

## Setup and Run

### 1. Backend setup

```powershell
cd Backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create `Backend/.env`:

```env
SECRET_KEY=replace-with-strong-secret
JWT_SECRET_KEY=replace-with-strong-jwt-secret

REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-app-password
```

If you keep environment variables in a file outside `Backend/.env`, set `PPA_ENV_FILE` before starting the server:

```powershell
cd Backend
$env:PPA_ENV_FILE="C:\secure\placement-portal.env"
```

If you are using `Backend/.env`, you can skip setting `PPA_ENV_FILE`.

Run the backend API:

```powershell
cd Backend
python app.py
```

Backend runs at `http://127.0.0.1:5000`.

### 2. Start Redis

If Redis is not already running, you can use Docker:

```powershell
docker run -d --name placement-redis -p 6379:6379 redis:7
```

### 3. Start Celery worker

From `Backend/`:

```powershell
$env:PPA_ENV_FILE="C:\secure\placement-portal.env"
celery -A app.celery worker --loglevel=info --pool=solo
```

### 4. Start Celery Beat (scheduler)

From `Backend/` in another terminal:

```powershell
$env:PPA_ENV_FILE="C:\secure\placement-portal.env"
celery -A app.celery beat --loglevel=info
```

### 5. Frontend setup

```powershell
cd Frontend
npm install
npm run dev
```

The frontend runs at `http://localhost:5173` (Vite default).

## Default Seeded Admin

On first backend run, an admin account is auto-seeded:

- Email: `admin123@gmail.com`
- Password: `admin123`

Update these credentials in production.

## Key Environment Variables

- `SECRET_KEY`: Flask app secret
- `JWT_SECRET_KEY`: JWT signing secret
- `REDIS_URL`: cache connection URL
- `CELERY_BROKER_URL`: Celery broker URL
- `CELERY_RESULT_BACKEND`: Celery result backend URL
- `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS`, `MAIL_USERNAME`, `MAIL_PASSWORD`: email configuration

## API Summary

### Auth

- `POST /api/auth/register`
- `POST /api/auth/login`

### Companies

- `GET /api/companies`
- `GET /api/companies/<id>`
- `PATCH /api/companies/<id>`
- `GET /api/companies/applications`
- `GET /api/companies/<id>/drives`

### Students

- `GET /api/students`
- `GET /api/students/<id>`
- `PATCH /api/students/<id>`
- `GET /api/students/<id>/drives`
- `GET /api/students/<student_id>/applications`
- `POST /api/students/<student_id>/applications` (multipart resume upload)
- `GET /api/students/applications`

### Drives

- `GET /api/drives`
- `POST /api/drives`
- `GET /api/drives/<id>`
- `PATCH /api/drives/<id>`
- `PUT /api/drives/<id>`
- `GET /api/drives/<id>/applications`

### Applications

- `GET /api/applications/<id>`
- `PATCH /api/applications/<id>`
- `GET /api/students/applications/<id>/resume`

### Export

- `POST /api/students/<student_id>/export-applications`
- `GET /api/export-status/<task_id>`
- `GET /api/exports/<filename>`

## Background Schedules

- `tasks.send_daily_reminders`: every day at 09:00 (server time)
- `tasks.send_monthly_activity_report`: 1st day of every month at 09:00 (server time)

## Operational Notes

- If Redis is down, cache falls back to in-memory automatically.
- Export and scheduled tasks require Celery worker and broker availability.
- Resume uploads are stored under `Backend/uploads/resumes/`.
- CSV exports are stored under `Backend/uploads/exports/`.
- Keep credentials out of version control; rotate any previously committed secrets.

## Troubleshooting

- `503 Task broker is unavailable` on export:
  - Start Redis and Celery worker.
- Login issues for company:
  - Company must be approved by admin first.
- Student/company blocked from login:
  - Their status may be `Blacklisted`.
- Frontend cannot reach backend:
  - Verify backend is running on `127.0.0.1:5000`.
  - Check `Frontend/src/services/api.js` base URL.
