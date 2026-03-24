from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True, nullable=False) # Reference to User Service ID
    specialization = Column(String, nullable=False)
    experience_years = Column(Integer, nullable=True)
    is_available = Column(Boolean, default=True)
