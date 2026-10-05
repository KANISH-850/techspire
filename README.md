# 🏥 TechSpire AI Hospital Management System

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.0-61DAFB?style=flat-square&logo=react)](https://react.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker)](https://www.docker.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Local_AI-000000?style=flat-square)](https://ollama.ai/)
[![License](https://img.shields.io/badge/Status-Deployment_Ready-emerald?style=flat-square)]()

**TechSpire** is an enterprise-grade AI Hospital Management System (HMS) prototype designed to unify clinical administration, on-premise generative AI assistance, machine learning forecasting, and dynamic executive report generation within a secure, containerized environment.

---

## 🌟 Key Features & Core Modules

### 1. 📊 CEO Executive AI Dashboard
- **Real-Time KPIs:** Tracks hospital revenue, patient volume, bed utilization, patient satisfaction, total admissions, discharges, and emergency cases.
- **Executive AI Insights:** Generates operational summaries, key insights, and priority recommendations powered by local AI.
- **Financial & Department Analytics:** Departmental revenue distribution charts and live system risk alerts.

### 2. 🩺 Clinical Operations & Patient Management
- **Patient Registry:** Canonical patient record management with MRN tracking, gender/age demographics, and contact info.
- **Appointments Management:** Outpatient appointment scheduling, department routing, and status tracking (Scheduled, Completed, Cancelled).
- **Inpatient Admissions:** Active inpatient tracking, admission/discharge logs, and ward assignment.
- **Bed Occupancy & Allocation:** Ward and ICU bed grid status overview (Cardiology, Neurology, Orthopedics, Emergency, Pediatrics).

### 3. 🤖 Local Hospital AI Chatbot (RAG Architecture)
- **On-Premise Privacy:** Runs **100% locally** inside an Ollama container using `Qwen3:4B` and `nomic-embed-text` embeddings—zero patient data sent to third-party cloud APIs.
- **Retrieval-Augmented Generation (RAG):** Integrates ChromaDB vector store (`hospital_knowledge` collection) with 500-character chunking and top-3 similarity search.
- **Real-Time Streaming:** Streams responses via Server-Sent Events (SSE) and persists complete conversation history in PostgreSQL.

### 4. 📈 Predictive AI Analytics Engine
- **Supervised ML Forecasting:** Scikit-Learn `RandomForestRegressor` models for Financial Revenue ($R^2 = 0.82$) and Inpatient Admissions ($R^2 = 0.74$).
- **Statistical Time-Series:** Bounded linear trend models for Ward Bed Occupancy and Moving Averages for Medicine Demand.
- **Deterministic Inventory Math:** Reorder Point formula ($RP = \text{Lead Time Usage} + \text{Safety Stock}$) for stockout risk calculation.

### 5. 📄 AI Report Builder
- **Dynamic PDF Generation:** Publication-ready PDF document rendering built with ReportLab.
- **Structured Excel Export:** Multi-tab financial and operational spreadsheets generated via OpenPyXL.
- **Report Types:** Executive Summaries, Financial Audits, Clinical Occupancy Reports, and Procurement Logs.

### 6. 📦 Inventory & AI Procurement Management
- **Stock Tracking:** Real-time medicine stock, category filters, and expiration alert tracking.
- **AI Order Recommendations:** Automated purchase order drafting with vendor management (PharmaCorp Ltd, MedSupply Global).

---

## 🏗️ Technical Architecture

TechSpire is architected as a **modular monolithic FastAPI backend** paired with a **React Single Page Application (SPA)**, containerized into a multi-service Docker stack:

```
                      +---------------------------------------+
                      |         Browser Client (SPA)          |
                      +-------------------+-------------------+
                                          |
                                    Port 8080 (HTTP)
                                          v
                      +-------------------+-------------------+
                      |      Nginx Reverse Proxy & React      |
                      |          (techspire_frontend)         |
                      +-------------------+-------------------+
                                          |
                                  /api/v1 Reverse Proxy
                                          v
                      +-------------------+-------------------+
                      |       FastAPI Application Server      |
                      |          (techspire_backend)          |
                      +---------+-------------------+---------+
                                |                   |
                 Port 5432 (SQL) |                   | Port 11434 (HTTP/JSON)
                                v                   v
          +---------------------+---+           +---+---------------------+
          | PostgreSQL 16 Database  |           |   Ollama Local AI Container |
          |    (techspire_db)       |           |     (techspire_ollama)      |
          +-------------------------+           +-------------------------+
          | - Relational Records    |           | - Qwen3:4B (LLM Engine) |
          | - Persistent Volumes    |           | - nomic-embed-text      |
          +-------------------------+           | - ChromaDB Vector Store |
                                                +-------------------------+
```

---

## 🛠️ Technology Stack

| Layer | Technology | Description |
| :--- | :--- | :--- |
| **Backend Framework** | FastAPI (Python 3.11) | Async REST API, Pydantic data validation, SSE streaming |
| **Database** | PostgreSQL 16 | Relational data store connected via SQLAlchemy 2.0 ORM |
| **Database Migrations**| Alembic | Version-controlled schema migrations (`001_initial_hms`) |
| **Frontend Framework** | React 19 + Vite | SPA framework with Tailwind CSS styling and Recharts |
| **Web Server** | Nginx (Alpine) | Reverse proxy, static asset hosting, SPA fallback routing |
| **Local AI Engine** | Ollama | On-premise container serving `qwen3:4b` LLM |
| **Vector Store** | ChromaDB | Embeddings vector database for local SOP document retrieval |
| **Embeddings Model** | `nomic-embed-text` | 768-dimensional text embedding model |
| **Predictive Analytics**| Scikit-Learn / Pandas | Machine learning regressors and statistical time-series |
| **Reporting** | ReportLab & OpenPyXL | Programmatic PDF and Excel file compilation |
| **Containerization** | Docker Compose | Multi-container orchestration with persistent volumes |

---

## 🔒 Security & Data Governance

- **Authentication:** OAuth2 Password Bearer flow issuing signed **HS256 JWT tokens**.
- **Password Security:** Salted password hashing via **Bcrypt** (`passlib[bcrypt]`).
- **SQL Injection Prevention:** 100% parameterized queries via SQLAlchemy 2.0 ORM.
- **Privacy-by-Design:** On-premise AI processing avoids external cloud API data transmission.
- **Environment Governance:** Configuration checks prevent default development secret keys in production.

---

## 🚀 Quick Start Guide

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
- Git installed.

### Option 1: Run with Docker Compose (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/KANISH-850/techspire.git
   cd techspire
   ```

2. **Start the complete stack:**
   ```bash
   docker compose up -d
   ```

3. **Verify running containers:**
   ```bash
   docker compose ps
   ```
   You should see 4 active containers:
   - `techspire_db` (Healthy on port `5432`)
   - `techspire_backend` (Running on port `8000`)
   - `techspire_frontend` (Running on port `8080`)
   - `techspire_ollama` (Running on port `11434`)

4. **Access the application:**
   - **Frontend UI:** [http://localhost:8080](http://localhost:8080)
   - **OpenAPI Documentation:** [http://localhost:8000/docs](http://localhost:8000/docs)

5. **Demo Credentials:**
   - **Username:** `admin`
   - **Password:** `admin123`

---

### Option 2: Run in Local Development Mode

#### Backend Setup
```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python app/db/seed.py
uvicorn app.main:app --reload --port 8000
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 🧪 Verification & Automated Testing

TechSpire includes a complete automated test suite validating APIs, database ORM models, security boundaries, and predictive analytics:

```bash
# Run pytest automated test suite
py -m pytest backend/tests

# Check Alembic database schema migrations
docker exec techspire_backend alembic check

# Verify production frontend build
cd frontend && npm run build
```

---

## 📂 Project Directory Structure

```
TechSpire/
├── docker-compose.yml              # Multi-container Docker orchestration
├── DEPLOYMENT.md                   # Complete deployment & architecture specification
├── backend/                        # FastAPI Backend Application
│   ├── Dockerfile                  # Backend container configuration
│   ├── requirements.txt            # Python dependencies
│   ├── alembic/                    # Database schema migration scripts
│   ├── app/
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── core/                   # Security, config, database, logging
│   │   ├── db/                     # Database seed data script
│   │   ├── models/                 # SQLAlchemy ORM models (13 tables)
│   │   ├── routers/                # API endpoint routers
│   │   ├── schemas/                # Pydantic data schemas
│   │   └── services/               # Clinical, AI RAG, ML & Report services
│   ├── rag/                        # RAG ingestion, chunking & vector store
│   └── tests/                      # Automated test suite (20/20 passing)
├── frontend/                       # React 19 Single Page Application
│   ├── Dockerfile                  # Nginx production build container
│   ├── nginx.conf                  # Reverse proxy & SPA fallback configuration
│   ├── package.json                # Frontend dependencies
│   └── src/
│       ├── App.jsx                 # SPA router and shell layout
│       ├── api/                    # API client integrations
│       ├── auth/                   # JWT Authentication context
│       ├── components/             # Reusable UI components
│       └── pages/                  # Module pages (Dashboard, Patients, Chatbot, etc.)
└── shared/                         # Shared themes and component assets
```

---

## 📝 License & Disclaimer

This project is built for **educational, research, and demonstration purposes**. It uses a synthetic dataset generated by `app/db/seed.py`. All patient names, medical records, and transaction metrics are completely fictitious.

---

<p align="center">
  Developed with ❤️ for Modern Healthcare Operations by <b>TechSpire Engineering Team</b>
</p>
