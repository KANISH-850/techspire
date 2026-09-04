# Architecture Overview

## High-Level Architecture

```
[React Frontend] (Vite, Tailwind, Recharts)
       ↓ (REST API via Axios)
[FastAPI Backend] (Python)
       ↓
   Service Layer (Analytics & AI Providers)
       ↓                                ↓
[PostgreSQL DB] (SQLAlchemy)       [OpenRouter]
       ↓                                ↓
(Models: Patient, Dept, Alert)     (DeepSeek AI)
```

## Backend Structure

The backend follows a domain-driven structure mapped heavily to typical FastAPI best practices:

- **`app/models/`**: SQLAlchemy models that define the PostgreSQL schema (`alert.py`, `department.py`, `patient.py`, `revenue.py`).
- **`app/schemas/`**: Pydantic models for strict API response validation.
- **`app/api/v1/`**: FastAPI routers grouping endpoints logically.
- **`app/services/analytics/`**: Complex metric aggregation logic that queries the DB (trends, percentage calculations, rule-based alerts).
- **`app/services/ai/`**: Provider integration logic ensuring structured prompt delivery and robust JSON fallback parsing for AI models.

## AI Integration

The dashboard doesn't just send raw strings to an LLM. It:
1. Pre-aggregates all KPIs, alerts, and department statuses.
2. Serializes this into a JSON context block.
3. Injects the context into an explicit prompt instructing the AI to act as a hospital executive.
4. Enforces a strict JSON structure for the response containing: Executive Summary, Risks, and Priority-ranked Recommendations.
5. Safely parses the response and gracefully handles malformed data.
