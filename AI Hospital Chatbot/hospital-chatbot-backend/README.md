# AI-001: Hospital AI Chatbot Backend

A production-ready FastAPI backend service acting as an intelligent hospital assistant. This is the foundational module designed to seamlessly integrate with a larger Hospital Management System (HMS).

## Features
- **Clean Architecture**: Clear separation of concerns using models, schemas, repositories, and services.
- **AI Abstraction**: Pluggable AI providers (OpenAI, Gemini, etc.) configured via `app/services/ai_provider.py`.
- **Database Layer**: Robust PostgreSQL setup with SQLAlchemy 2.0 and connection pooling.
## Tech Stack
- Python 3.12+
- FastAPI & Uvicorn
- PostgreSQL
- SQLAlchemy 2.0
- Pydantic v2
## Setup Instructions

### 1. Environment Configuration
Copy the `.env.example` template to a new `.env` file:
```bash
cp .env.example .env
```
Open `.env` and fill in your database credentials and AI Provider API keys.

### 2. Running Locally

If you prefer running natively on your machine:

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Database Setup**: Start a local PostgreSQL instance and ensure your `.env` variables point to it.
4. **Run the server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Documentation
Once the server is running, access the interactive API documentation at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Project Structure Overview
```
app/
├── api/          # FastAPI route definitions (v1)
├── core/         # Core config, DB engine configuration, and logging
├── models/       # SQLAlchemy ORM models (User, Conversation, Message)
├── repositories/ # Data access layer (Repository Pattern)
├── schemas/      # Pydantic models for request/response validation
├── services/     # Business logic and AI provider abstraction
└── shared/       # Shared exceptions and base response schemas
```
