from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.security import get_current_user
from app.db.session import get_db
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate
from app.models.user import User
from app.services.user_service import UserService

router = APIRouter()

@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Ensure the requester is authenticated
):
    user_service = UserService(db)

    # Ensure the user creating another user has proper permissions (e.g., admin)
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create a new user."
        )

    return user_service.create_user(user_in)

@router.get("/{username}", response_model=UserSchema)
def get_user_by_username(
    username: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Ensure the requester is authenticated
):
    user_service = UserService(db)
    user = user_service.get_user_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    return user

@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Ensure the requester is authenticated
):
    user_service = UserService(db)

    # Ensure the user updating another user has proper permissions (e.g., admin)
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this user."
        )

    return user_service.update_user(user_id, user_in)

@router.delete("/{user_id}", response_model=UserSchema)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Ensure the requester is authenticated
):
    user_service = UserService(db)

    # Ensure the user deleting another user has proper permissions (e.g., admin)
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this user."
        )

    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    user_service.deactivate_user(user_id)
    return user

@router.get("/", response_model=List[UserSchema])
def list_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Ensure the requester is authenticated
):
    user_service = UserService(db)
    return user_service.list_users(skip=skip, limit=limit)

@router.put("/{user_id}/password", response_model=UserSchema)
def update_user_password(
    user_id: int,
    new_password: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Ensure the requester is authenticated
):
    user_service = UserService(db)

    # Ensure the user updating another user's password has proper permissions
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this user's password."
        )

    return user_service.update_user_password(user_id, new_password)

@router.put("/{user_id}/deactivate", response_model=UserSchema)
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Ensure the requester is authenticated
):
    user_service = UserService(db)

    # Ensure the user deactivating another user has proper permissions (e.g., admin)
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to deactivate this user."
        )

    return user_service.deactivate_user(user_id)

@router.put("/{user_id}/activate", response_model=UserSchema)
def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Ensure the requester is authenticated
):
    user_service = UserService(db)

    # Ensure the user activating another user has proper permissions (e.g., admin)
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to activate this user."
        )

    return user_service.activate_user(user_id)
