from fastapi import FastAPI
from app.db.database import engine, Base
from app.api import doctor_api

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ScalabixMedical - Doctor Service")

app.include_router(doctor_api.router, prefix="/api/v1/doctors", tags=["doctors"])

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "doctor_service"}
