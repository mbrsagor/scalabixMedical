from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, status, Header
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.doctor_schema import DoctorResponse, DoctorCreate, DoctorWithUserInfo
from app.models.model import Doctor
from app.repositories.doctor_repository import doctor_repository
from app.services.doctor_service import UserServiceIntegration
from app.utils import custom_response

router = APIRouter()

def get_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    return authorization.split(" ")[1]


@router.post("/")
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
        error_resp = custom_response.prepare_error_response("User role is not assigned as doctor")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=error_resp)

    # Check if doctor already exists
    existing_doc = doctor_repository.get_by_user_id(db, user_id=doctor_in.user_id)
    if existing_doc:
         error_resp = custom_response.prepare_error_response("Doctor profile already exists for this user")
         return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=error_resp)

    doctor = doctor_repository.create(db, obj_in=doctor_in)
    doctor_data = DoctorResponse.model_validate(doctor).model_dump()
    return custom_response.prepare_success_response(data=doctor_data)


@router.get("/doctor/{doctor_id}")
async def read_doctor(
    doctor_id: int, 
    db: Session = Depends(get_db),
    token: str = Depends(get_token)
):
    doctor = doctor_repository.get(db, doctor_id=doctor_id)
    if not doctor:
        error_resp = custom_response.prepare_error_response("Doctor not found")
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=error_resp)
    
    # Fetch additional user info to enrich the response
    user_info = await UserServiceIntegration.get_user_info(doctor.user_id, token)
    
    # Build complete response
    response_data = doctor.__dict__.copy()
    response_data.pop("_sa_instance_state", None)
    response_data["user_info"] = user_info
    
    return custom_response.prepare_success_response(data=response_data)
