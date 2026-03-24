from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, status, Header, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.utils import custom_response, messages
from app.repositories.appointment_repository import appointment_repository
from app.services.integration_service import IntegrationService
from app.schemas.appointment_schema import AppointmentCreate, AppointmentUpdate, AppointmentResponse, AppointmentDetailedResponse

router = APIRouter()

# Dependency to get token from header
def get_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail=messages.INVALID_AUTH_HEADER)
    return authorization.split(" ")[1]

@router.post("/")
async def create_appointment(
    appointment_in: AppointmentCreate, 
    db: Session = Depends(get_db),
    token: str = Depends(get_token)
):
    # Verify the patient exists in the User Service
    try:
        patient_info = await IntegrationService.get_user_info(appointment_in.patient_user_id, token)
    except HTTPException as exc:
        error_resp = custom_response.prepare_error_response(exc.detail)
        return JSONResponse(status_code=exc.status_code, content=error_resp)

    # Verify the doctor exists in the Doctor Service
    try:
        doctor_info = await IntegrationService.get_doctor_info(appointment_in.doctor_id, token)
    except HTTPException as exc:
        error_resp = custom_response.prepare_error_response(exc.detail)
        return JSONResponse(status_code=exc.status_code, content=error_resp)
    
    # Create the appointment
    appointment = appointment_repository.create(db, obj_in=appointment_in)
    appointment_data = AppointmentResponse.model_validate(appointment).model_dump()
    return custom_response.prepare_success_response(data=appointment_data)

@router.get("/appointment/{appointment_id}")
async def read_appointment(
    appointment_id: int, 
    db: Session = Depends(get_db),
    token: str = Depends(get_token)
):
    appointment = appointment_repository.get(db, appointment_id=appointment_id)
    if not appointment:
        error_resp = custom_response.prepare_error_response(messages.APPOINTMENT_NOT_FOUND)
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=error_resp)
    
    # Fetch additional info from external services for detailed view
    try:
        patient_info = await IntegrationService.get_user_info(appointment.patient_user_id, token)
        doctor_info = await IntegrationService.get_doctor_info(appointment.doctor_id, token)
    except HTTPException as exc:
        error_resp = custom_response.prepare_error_response(exc.detail)
        return JSONResponse(status_code=exc.status_code, content=error_resp)
    
    response_data = appointment.__dict__.copy()
    response_data.pop("_sa_instance_state", None)
    response_data["patient_info"] = patient_info
    response_data["doctor_info"] = doctor_info
    
    return custom_response.prepare_success_response(data=response_data)

@router.get("/patient/{patient_user_id}")
async def read_patient_appointments(
    patient_user_id: int, 
    db: Session = Depends(get_db),
    token: str = Depends(get_token)
):
    appointments = appointment_repository.get_all_for_patient(db, patient_user_id=patient_user_id)
    appointments_data = [AppointmentResponse.model_validate(app).model_dump() for app in appointments]
    return custom_response.prepare_success_response(data=appointments_data)

@router.get("/doctor/{doctor_id}")
async def read_doctor_appointments(
    doctor_id: int, 
    db: Session = Depends(get_db),
    token: str = Depends(get_token)
):
    appointments = appointment_repository.get_all_for_doctor(db, doctor_id=doctor_id)
    appointments_data = [AppointmentResponse.model_validate(app).model_dump() for app in appointments]
    return custom_response.prepare_success_response(data=appointments_data)

@router.put("/appointment/{appointment_id}")
async def update_appointment(
    appointment_id: int, 
    appointment_in: AppointmentUpdate, 
    db: Session = Depends(get_db),
    token: str = Depends(get_token)
):
    existing_appointment = appointment_repository.get(db, appointment_id=appointment_id)
    if not existing_appointment:
        error_resp = custom_response.prepare_error_response(messages.APPOINTMENT_NOT_FOUND)
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=error_resp)
        
    appointment = appointment_repository.update(db, db_obj=existing_appointment, obj_in=appointment_in)
    appointment_data = AppointmentResponse.model_validate(appointment).model_dump()
    return custom_response.prepare_success_response(data=appointment_data)
