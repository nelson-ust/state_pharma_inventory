from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.core.security import create_access_token, verify_password
from app.db.session import get_db
from app.models.user import User
from app.services import user_service
from app.services.user_service import UserService
from app.schemas.user import Token
from app.core.config import settings

router = APIRouter()

@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    
    # Authenticate the user
    user = user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create the access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Optionally, add a route to refresh tokens (if using refresh tokens)
@router.post("/refresh", response_model=Token)
def refresh_access_token(
    current_user: User = Depends(user_service.get_current_user),
    db: Session = Depends(get_db)
):
    user_service = UserService(db)

    # You might check if the user's session is still valid or implement other logic
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
