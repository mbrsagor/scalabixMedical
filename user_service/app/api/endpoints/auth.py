from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.db.database import get_db
from app.utils import custom_response
from app.core.config import settings
from app.repositories.user import user_repository
from app.core.security import verify_password, create_access_token
from app.schemas.user import Token, UserResponse, UserCreate, UserLogin

router = APIRouter()

# Login Route
@router.post("/login")
def login_access_token(user_in: UserLogin, db: Session = Depends(get_db)):
    user = user_repository.get_by_email(db, email=user_in.email)
    if not user or not verify_password(user_in.password, user.hashed_password):
        return custom_response.prepare_error_response("Incorrect email or password")
        # raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        return custom_response.prepare_error_response("Inactive user")
        # raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    resp = custom_response.prepare_login_response(
        token=create_access_token(user.id, expires_delta=access_token_expires),
        role=user.role,
        email=user.email,
        full_name=f"{user.first_name} {user.last_name}",
    )
    return resp

# Register Route
@router.post("/register")
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    user = user_repository.get_by_email(db, email=user_in.email)
    if user:
        return custom_response.prepare_error_response("The user with this username already exists in the system.")
    user = user_repository.create(db, obj_in=user_in)
    # The custom response needs a dict or serializable object. Pydantic models need .model_dump() or similar, 
    # but SQLAlchemy objects can be problematic directly. 
    # We will pass the UserResponse schema to serialize it first, then pass to custom response
    user_data = UserResponse.model_validate(user).model_dump()
    return custom_response.prepare_register_response(user_data)
