from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status  # Import HTTPException and status codes
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.repositories.base import BaseRepository
from app.core.security import get_password_hash

class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_by_username(self, username: str) -> Optional[User]:
        """
        Retrieve a user by their username.
        """
        try:
            return self.db.query(User).filter(User.username == username).first()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while retrieving the user with username {username}.",
            )

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email.
        """
        try:
            return self.db.query(User).filter(User.email == email).first()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while retrieving the user with email {email}.",
            )

    def create(self, obj_in: UserCreate) -> User:
        """
        Create a new user with hashed password.
        """
        obj_in.password_hash = get_password_hash(obj_in.password)
        return super().create(obj_in)

    def update_user_password(self, db_obj: User, new_password: str) -> User:
        """
        Update a user's password.
        """
        db_obj.password_hash = get_password_hash(new_password)
        return super().update(db_obj, db_obj)

    def deactivate_user(self, db_obj: User) -> User:
        """
        Deactivate a user.
        """
        db_obj.is_active = False
        return super().update(db_obj, db_obj)

    def activate_user(self, db_obj: User) -> User:
        """
        Activate a user.
        """
        db_obj.is_active = True
        return super().update(db_obj, db_obj)
