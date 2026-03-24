from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.doctor import DoctorResponse, DoctorCreate, DoctorWithUserInfo
from app.models.doctor import Doctor
from app.repositories.doctor import doctor_repository
from app.services.doctor_service import UserServiceIntegration

router = APIRouter()

def get_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    return authorization.split(" ")[1]


@router.post("/", response_model=DoctorResponse)
async def create_doctor(
    doctor_in: DoctorCreate, 
    db: Session = Depends(get_db),
    token: str = Depends(get_token)
):
    # Verify user exists and is authorized to be a doctor (e.g. via User Service)
    # The get_user_info call acts as our service-to-service validation
    user_info = await UserServiceIntegration.get_user_info(doctor_in.user_id, token)
    
    # We can also verify the user's role is 'doctor' here based on what we get back
    if user_info.get("role") != "doctor":
        raise HTTPException(status_code=400, detail="User role is not assigned as doctor")

    # Check if doctor already exists
    existing_doc = doctor_repository.get_by_user_id(db, user_id=doctor_in.user_id)
    if existing_doc:
         raise HTTPException(status_code=400, detail="Doctor profile already exists for this user")

    doctor = doctor_repository.create(db, obj_in=doctor_in)
    return doctor


@router.get("/doctor/{doctor_id}", response_model=DoctorWithUserInfo)
async def read_doctor(
    doctor_id: int, 
    db: Session = Depends(get_db),
    token: str = Depends(get_token)
):
    doctor = doctor_repository.get(db, doctor_id=doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    # Fetch additional user info to enrich the response
    user_info = await UserServiceIntegration.get_user_info(doctor.user_id, token)
    
    # Build complete response
    response_data = doctor.__dict__.copy()
    response_data["user_info"] = user_info
    
    return response_data
