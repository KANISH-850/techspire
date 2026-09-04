# API Documentation

Base URL: `/api/v1`

## Dashboard Endpoints

### 1. KPI Summary
`GET /dashboard/kpis`
- **Query Params**: `start_date`, `end_date`, `department_id`
- **Description**: Returns top-level aggregated metrics including totals, previous period comparisons, and percentage trends.
- **Response Schema**: `KPISummary`

### 2. Revenue Insights
`GET /dashboard/revenue`
- **Query Params**: `start_date`, `end_date`, `department_id`
- **Description**: Returns total revenue, a month-by-month breakdown, department breakdowns, and overall growth.
- **Response Schema**: `RevenueInsights`

### 3. Department Performance
`GET /dashboard/departments`
- **Query Params**: `start_date`, `end_date`
- **Description**: Returns granular metrics (patient count, occupancy, revenue, satisfaction) and a calculated performance score for each department.
- **Response Schema**: `DepartmentList`

### 4. Alerts
`GET /dashboard/alerts`
- **Description**: Combines active seeded alerts from the database with dynamically generated rule-based alerts (e.g. occupancy > 90%) based on current data.
- **Response Schema**: `AlertList`

### 5. AI Insights
`GET /dashboard/ai-insights`
- **Description**: Aggregates data from KPIs, Departments, and Alerts, sends it to the AI Provider, and returns structured executive insights.
- **Response Schema**: `AIInsights`

## Health Check
`GET /health`
- **Description**: Basic system health check.
