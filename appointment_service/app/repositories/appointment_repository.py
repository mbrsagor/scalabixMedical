from sqlalchemy.orm import Session
from app.models.model import Appointment
from app.schemas.appointment_schema import AppointmentCreate, AppointmentUpdate

class AppointmentRepository:
    def get(self, db: Session, appointment_id: int):
        return db.query(Appointment).filter(Appointment.id == appointment_id).first()

    def get_all_for_patient(self, db: Session, patient_user_id: int):
        return db.query(Appointment).filter(Appointment.patient_user_id == patient_user_id).all()

    def get_all_for_doctor(self, db: Session, doctor_id: int):
        return db.query(Appointment).filter(Appointment.doctor_id == doctor_id).all()

    def create(self, db: Session, obj_in: AppointmentCreate):
        db_obj = Appointment(
            patient_user_id=obj_in.patient_user_id,
            doctor_id=obj_in.doctor_id,
            appointment_time=obj_in.appointment_time,
            status=obj_in.status
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Appointment, obj_in: AppointmentUpdate):
        if obj_in.appointment_time is not None:
            db_obj.appointment_time = obj_in.appointment_time
        if obj_in.status is not None:
            db_obj.status = obj_in.status
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Appointment):
        db.delete(db_obj)
        db.commit()
        return db_obj

appointment_repository = AppointmentRepository()
