from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserResponse
from app.models.user import User, Role
from app.services.user_service import get_current_active_user, RoleChecker
from app.repositories.user import user_repository

router = APIRouter()

# Get current user
@router.get("/me", response_model=UserResponse)
def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# Get user by id
@router.get("/{user_id}", response_model=UserResponse)
def read_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    user = user_repository.get(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Only admins or the user themselves can view this profile
    if current_user.id != user_id and current_user.role != Role.ADMIN:
        # Also let doctors view profiles (this could be restricted further later)
        if current_user.role != Role.DOCTOR:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    return user

# Example of an RBAC protected endpoint: Only admins can list all users
@router.get("/", response_model=list[UserResponse], dependencies=[Depends(RoleChecker([Role.ADMIN]))])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users
