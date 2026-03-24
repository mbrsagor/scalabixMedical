from fastapi import FastAPI
from app.db.database import engine, Base
from app.api import appointment_api

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ScalabixMedical - Appointment Service")

app.include_router(appointment_api.router, prefix="/api/v1/appointments", tags=["appointments"])

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "appointment_service"}
