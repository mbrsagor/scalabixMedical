from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, status

from app.db.database import get_db
from app.utils import custom_response
from app.core.config import settings
from app.repositories.user_repository import user_repository
from app.core.security import verify_password, create_access_token
from app.schemas.user_schema import Token, UserResponse, UserCreate, UserLogin

router = APIRouter()

# Login Route
@router.post("/login")
def login_access_token(user_in: UserLogin, db: Session = Depends(get_db)):
    # Get user by email
    user = user_repository.get_by_email(db, email=user_in.email)

    # Check if user exists and password is correct
    if not user or not verify_password(user_in.password, user.hashed_password):
        error_resp = custom_response.prepare_error_response("Incorrect email or password")
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=error_resp)

    # Check if user is active
    elif not user.is_active:
        error_resp = custom_response.prepare_error_response("Inactive user")
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=error_resp)
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # Custom response
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
    # Get user by email
    user = user_repository.get_by_email(db, email=user_in.email)
    
    # Check if user exists
    if user:
        error_resp = custom_response.prepare_error_response("The user with this email already exists in the system.")
        return JSONResponse(status_code=400, content=error_resp)
    
    # Create user
    user = user_repository.create(db, obj_in=user_in)
    user_data = UserResponse.model_validate(user).model_dump()
    return custom_response.prepare_register_response(user_data)
