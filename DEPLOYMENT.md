# TechSpire AI Hospital Management System — Production Deployment Guide

## Architecture Overview

TechSpire is a unified enterprise AI Hospital Management System consisting of:
1. **Single FastAPI Backend** (`backend/`): Standardized on SQLAlchemy 2.0 ORM, PostgreSQL database (`hospital_management_system`), JWT authentication (`/api/v1/auth`), structured health endpoints (`/health`), and REST APIs across 5 integrated domains.
2. **Single React Frontend** (`frontend/`): Vite + React 18 frontend with unified dark glassmorphism design system, persistent session routing, and dynamic module navigation.
3. **Database** (`PostgreSQL 16`): Single canonical database `hospital_management_system` storing admissions, bed allocations, financial transactions, inventory, procurement, and audit logs.
4. **Local LLM Engine** (`Ollama`): Self-hosted Ollama container providing local LLM (`qwen3:4b`) and vector embeddings (`nomic-embed-text`) for AI Clinical Chatbot RAG and Executive AI Insights.

---

## 1. Prerequisites & System Requirements

- **Operating System**: Linux (Ubuntu 22.04+ recommended) or Windows 10/11 with WSL2 / Docker Desktop
- **Docker & Docker Compose**: Docker Engine 24+ and Docker Compose v2+
- **Python**: Python 3.11+ (if running locally without Docker)
- **Node.js**: Node.js 18+ & npm 9+ (if running frontend locally)
- **PostgreSQL**: PostgreSQL 16+ (if running database locally)
- **Ollama**: Ollama binary or Docker image (`ollama/ollama:latest`)

---

## 2. Environment Configuration

Copy `.env.example` to `.env` in `backend/` and configure production secrets.

### Required Environment Variables (`backend/.env`)

```env
# Database Settings
DATABASE_URL=postgresql://postgres:YOUR_SECURE_PASSWORD@db:5432/hospital_management_system
POSTGRES_USER=postgres
POSTGRES_PASSWORD=YOUR_SECURE_PASSWORD
POSTGRES_DB=hospital_management_system

# Application Security
SECRET_KEY=YOUR_RAILS_OR_HS256_PRODUCTION_SECRET_KEY_MIN_32_CHARS
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ENVIRONMENT=production

# Seed Admin Credentials (Idempotent initial setup)
SEED_ADMIN_USERNAME=admin
SEED_ADMIN_PASSWORD=YOUR_ADMIN_PASSWORD
SEED_ADMIN_EMAIL=admin@techspire.hospital

# AI & LLM Service Settings (Ollama Container)
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=qwen3:4b
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
```

> **Security Note**: In `ENVIRONMENT=production`, backend startup enforces non-default values for `SECRET_KEY` and `DATABASE_URL`. Startup will fail with a `ValueError` if default credentials are detected.

---

## 3. Docker Compose Deployment (Recommended)

### Step 1: Clone & Configure
```bash
git clone https://github.com/KANISH-850/techspire.git
cd techspire
cp backend/.env.example backend/.env
# Edit backend/.env with your production passwords and secrets
```

### Step 2: Build & Start Services
```bash
docker compose up -d --build
```

### Step 3: Initialize Database Schema & Seed Data
```bash
# Run database migrations via Alembic inside backend container
docker compose exec backend alembic upgrade head

# Run initial seed script (idempotent seed for admin user & historical records)
docker compose exec backend python app/db/seed.py
```

### Step 4: Pull Required Ollama LLM Models
```bash
# Download LLM model for Chatbot & Dashboard AI Insights
docker compose exec ollama ollama pull qwen3:4b

# Download Embedding model for Vector RAG search
docker compose exec ollama ollama pull nomic-embed-text
```

---

## 4. Local Native Deployment (Alternative)

### Step 1: PostgreSQL Setup
```bash
# Create PostgreSQL Database
psql -U postgres -c "CREATE DATABASE hospital_management_system;"
```

### Step 2: Backend Setup
```bash
cd backend
python -m venv venv
# On Windows: venv\Scripts\activate | On Linux: source venv/bin/activate
pip install -r requirements.txt

# Run migrations & seed
alembic upgrade head
python app/db/seed.py

# Start Backend Server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Step 3: Frontend Setup
```bash
cd frontend
npm install
npm run build
npm run preview -- --port 80 --host 0.0.0.0
```

---

## 5. System Verification & Health Check Endpoints

Verify all components are active:

| Endpoint | Method | Expected Output | Purpose |
|---|---|---|---|
| `http://localhost:8000/health` | GET | `{"status": "healthy", "database": "connected", "ollama": "available"}` | Full System Status |
| `http://localhost:8000/docs` | GET | OpenAPI Interactive Swagger Docs | API Exploration |
| `http://localhost:8000/api/v1/auth/token` | POST | OAuth2 JWT Token (`access_token`) | Authentication Test |
| `http://localhost/` | GET | HTTP 200 (Single React SPA Interface) | Frontend Application |

### Verification Commands:
```bash
# Check Alembic Migration Sync Status (Must return 0 drift)
docker compose exec backend alembic check

# Run Automated Integration Tests (20/20 Test Cases)
docker compose exec backend pytest
```

---

## 6. Security & Hardening Checklist

- [x] **No Plaintext Passwords**: DB and JWT secrets loaded strictly via environment variables.
- [x] **Startup Validation**: In production mode, backend rejects default secrets and fails fast.
- [x] **Password Hashing**: Passwords stored using `bcrypt` (Passlib).
- [x] **JWT Validation**: Authenticated endpoints protected by `get_current_user` dependency.
- [x] **CORS Configuration**: Restricts origins in production mode (`backend/app/main.py`).
- [x] **Container Isolation**: Postgres data persisted in isolated named volume `techspire_postgres_data`.
- [x] **Ollama Isolation**: Model weights cached in isolated volume `techspire_ollama_data`.

---

## 7. Troubleshooting & FAQ

### Issue: Backend container crashes on startup with `ValueError: SECRET_KEY must be configured`
- **Solution**: Ensure `ENVIRONMENT=production` has a strong `SECRET_KEY` set in `backend/.env` (do not use default text).

### Issue: Database migration returns `Target database is not up to date`
- **Solution**: Execute `docker compose exec backend alembic upgrade head` to align schema with current models.

### Issue: Ollama returns connection refused on RAG queries
- **Solution**: Ensure the `ollama` container is running and accessible at `http://ollama:11434`. Pull models with `ollama pull qwen3:4b`.
