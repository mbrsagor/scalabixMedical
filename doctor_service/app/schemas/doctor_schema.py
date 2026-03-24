from pydantic import BaseModel
from typing import Optional

class DoctorBase(BaseModel):
    user_id: int
    specialization: str
    experience_years: Optional[int] = None
    is_available: bool = True

class DoctorCreate(DoctorBase):
    pass

class DoctorResponse(DoctorBase):
    id: int

    class Config:
        from_attributes = True

# Used to structure the combined response for a doctor + user info
class DoctorWithUserInfo(DoctorResponse):
    user_info: dict
