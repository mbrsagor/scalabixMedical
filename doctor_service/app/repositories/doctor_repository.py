from sqlalchemy.orm import Session
from app.models.model import Doctor
from app.schemas.doctor_schema import DoctorCreate

class DoctorRepository:
    def get(self, db: Session, doctor_id: int):
        return db.query(Doctor).filter(Doctor.id == doctor_id).first()

    def get_by_user_id(self, db: Session, user_id: int):
        return db.query(Doctor).filter(Doctor.user_id == user_id).first()

    def create(self, db: Session, obj_in: DoctorCreate):
        db_obj = Doctor(
            user_id=obj_in.user_id,
            specialization=obj_in.specialization,
            experience_years=obj_in.experience_years,
            is_available=obj_in.is_available
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

doctor_repository = DoctorRepository()
