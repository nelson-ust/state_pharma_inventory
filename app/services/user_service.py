from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from app.core.security import get_password_hash, verify_password
from fastapi import HTTPException, status
import logging

class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def create_user(self, user_in: UserCreate) -> User:
        try:
            # Check if the username or email already exists
            if self.user_repo.get_by_username(user_in.username):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="A user with this username already exists."
                )

            if self.user_repo.get_by_email(user_in.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="A user with this email already exists."
                )

            # Hash the password before saving the user
            user_in.password_hash = get_password_hash(user_in.password)

            # Create the user
            return self.user_repo.create(user_in)
        except IntegrityError as e:
            logging.error(f"Integrity error while creating user: {e}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A conflict occurred while creating the user. The username or email might already exist."
            )
        except SQLAlchemyError as e:
            logging.error(f"Database error while creating user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the user."
            )

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        try:
            # Retrieve the user by username
            user = self.user_repo.get_by_username(username)
            if not user:
                return None

            # Verify the provided password
            if not verify_password(password, user.password_hash):
                return None

            return user
        except SQLAlchemyError as e:
            logging.error(f"Database error while authenticating user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while authenticating the user."
            )

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        try:
            return self.user_repo.get(user_id)
        except SQLAlchemyError as e:
            logging.error(f"Database error while fetching user by ID: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while retrieving the user by ID."
            )

    def get_user_by_username(self, username: str) -> Optional[User]:
        try:
            return self.user_repo.get_by_username(username)
        except SQLAlchemyError as e:
            logging.error(f"Database error while fetching user by username: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while retrieving the user by username."
            )

    def get_user_by_email(self, email: str) -> Optional[User]:
        try:
            return self.user_repo.get_by_email(email)
        except SQLAlchemyError as e:
            logging.error(f"Database error while fetching user by email: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while retrieving the user by email."
            )

    def update_user(self, user_id: int, user_in: UserUpdate) -> Optional[User]:
        try:
            # Retrieve the user to update
            user = self.user_repo.get(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found."
                )

            # Update the user details
            return self.user_repo.update(user, user_in)
        except IntegrityError as e:
            logging.error(f"Integrity error while updating user: {e}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A conflict occurred while updating the user. This might be due to unique constraints."
            )
        except SQLAlchemyError as e:
            logging.error(f"Database error while updating user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the user."
            )

    def update_user_password(self, user_id: int, new_password: str) -> Optional[User]:
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found."
                )
            
            # Update the user's password
            return self.user_repo.update_user_password(user, new_password)
        except SQLAlchemyError as e:
            logging.error(f"Database error while updating user password: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the user's password."
            )

    def deactivate_user(self, user_id: int) -> Optional[User]:
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found."
                )

            return self.user_repo.deactivate_user(user)
        except SQLAlchemyError as e:
            logging.error(f"Database error while deactivating user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while deactivating the user."
            )

    def activate_user(self, user_id: int) -> Optional[User]:
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found."
                )

            return self.user_repo.activate_user(user)
        except SQLAlchemyError as e:
            logging.error(f"Database error while activating user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while activating the user."
            )

    def list_users(self, skip: int = 0, limit: int = 10) -> List[User]:
        try:
            return self.user_repo.get_multi(skip=skip, limit=limit)
        except SQLAlchemyError as e:
            logging.error(f"Database error while listing users: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while listing users."
            )
