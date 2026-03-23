from sqlalchemy.orm import Session
from app.models.model import User
from app.schemas.user_schema import UserCreate
from app.core.security import get_password_hash


class UserRepository(object):

    # Get user by id
    def get(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    # Get user by email
    def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()
    
    # Create user
    def create(self, db: Session, obj_in: UserCreate):
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            role=obj_in.role
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

user_repository = UserRepository()
