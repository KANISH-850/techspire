| Module | Endpoint | Method | Status | Real Data | Result |
|--------|----------|--------|--------|-----------|--------|
| Dashboard KPIs | /dashboard/kpis | GET | 200 | Yes | PASS |
| Dashboard Revenue | /dashboard/revenue | GET | 500 | N/A | FAIL (Internal Server Error) |
| Dashboard Depts | /dashboard/departments | GET | 200 | Yes | PASS |
| Dashboard Alerts | /dashboard/alerts | GET | 200 | Yes | PASS |
| Dashboard Insights | /dashboard/ai-insights | GET | 200 | Yes | PASS |
| Predictive Revenue | /predictive/revenue | GET | 200 | Yes | PASS |
| Predictive Admissions | /predictive/admissions | GET | 200 | Yes | PASS |
| Predictive Beds | /predictive/beds | GET | 200 | Yes | PASS |
| Predictive Medicines | /predictive/medicines | GET | 200 | Yes | PASS |
| Predictive Inventory | /predictive/inventory | GET | 200 | Yes | PASS |
| Report Templates | /reports/templates | GET | 200 | Yes | PASS |
| Report Gen (Fin, PDF) | /reports/generate?type=financial&format=pdf | GET | 200 | Yes | PASS (File downloaded) |
| Report Gen (Clin, Excel) | /reports/generate?type=clinical&format=excel | GET | 200 | Yes | PASS (File downloaded) |
| Report Gen (Inv, PDF) | /reports/generate?type=inventory&format=pdf | GET | 200 | Yes | PASS (File downloaded) |
| Report Gen (Proc, Excel) | /reports/generate?type=procurement&format=excel | GET | 200 | Yes | PASS (File downloaded) |
| Inventory Status | /inventory/status | GET | 200 | Yes | PASS |
| Inventory Low Stock | /inventory/low-stock | GET | 200 | Yes | PASS |
| Inventory Expiring | /inventory/expiring | GET | 200 | Yes | PASS |
| Inventory Vendors | /inventory/vendors | GET | 200 | Yes | PASS |
| Inventory Reorder | /inventory/reorder | GET | 200 | Yes | PASS |
| Inventory Recommendations | /inventory/recommendations | GET | 200 | Yes | PASS |
| Create PO | /inventory/purchase-orders | POST | 200 | Yes | PASS |
