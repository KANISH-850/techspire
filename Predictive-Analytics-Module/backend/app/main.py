from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.predictive import router as predictive_router

app = FastAPI(
    title="Predictive AI Analytics API",
    description="Independent plug-and-play module for hospital forecasting.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predictive_router, prefix="/api/v1/predictive", tags=["Predictive Analytics"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
