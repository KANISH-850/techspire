from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import inventory

app = FastAPI(title="AI Procurement & Inventory API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inventory.router, prefix="/api/v1/inventory", tags=["Inventory"])

@app.get("/health")
def health_check():
    return {"status": "ok", "module": "AI-Procurement"}
