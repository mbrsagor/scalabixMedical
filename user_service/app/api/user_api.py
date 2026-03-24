from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.model import User, Role
from app.utils import custom_response
from app.schemas.user_schema import UserResponse
from app.repositories.user_repository import user_repository
from app.services.user_service import get_current_active_user, RoleChecker

router = APIRouter()

# Get user by id
@router.get("/user/{user_id}", response_model=UserResponse)
def read_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    user = user_repository.get(db, user_id=user_id)
    if not user:
        error_response = custom_response.prepare_error_response("User not found")
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=error_resp)
    
    # Only admins or the user themselves can view this profile
    if current_user.id != user_id and current_user.role != Role.ADMIN:
        # Also let doctors view profiles (this could be restricted further later)
        if current_user.role != Role.DOCTOR:
            error_response = custom_response.prepare_error_response("Not enough permissions")
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=error_response)
    return user

# Example of an RBAC protected endpoint: Only admins can list all users
@router.get("/", response_model=list[UserResponse], dependencies=[Depends(RoleChecker([Role.ADMIN]))])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users
