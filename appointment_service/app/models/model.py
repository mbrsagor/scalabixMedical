from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import Base
from datetime import datetime

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_user_id = Column(Integer, index=True)
    doctor_id = Column(Integer, index=True)
    appointment_time = Column(DateTime, nullable=False)
    status = Column(String(50), default="Scheduled") # Scheduled, Completed, Cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
