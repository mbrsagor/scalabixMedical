from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AppointmentBase(BaseModel):
    patient_user_id: int
    doctor_id: int
    appointment_time: datetime
    status: Optional[str] = "Scheduled"

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    appointment_time: Optional[datetime] = None
    status: Optional[str] = None

class AppointmentResponse(AppointmentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Extended schema to hold the fetched details of patient and doctor
class AppointmentDetailedResponse(AppointmentResponse):
    patient_info: dict
    doctor_info: dict
