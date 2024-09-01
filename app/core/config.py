
# # app/core/config.py
# import os
# from dotenv import load_dotenv

# # Load the environment variables from the .env file
# load_dotenv()

# class Settings:
#     DATABASE_USER: str = os.getenv("DATABASE_USER")
#     DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD")
#     DATABASE_HOST: str = os.getenv("DATABASE_HOST")
#     DATABASE_PORT: str = os.getenv("DATABASE_PORT")
#     DATABASE_NAME: str = os.getenv("DATABASE_NAME")

#     SQLALCHEMY_DATABASE_URI = (
#         f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}"
#         f"@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
#     )

# settings = Settings()


import os
from dotenv import load_dotenv
from pydantic import BaseSettings

# Load environment variables from a .env file
load_dotenv()

class Settings(BaseSettings):
    # General application settings
    APP_NAME: str = "Pharmaceutical Inventory System"
    DEBUG: bool = False

    # Database settings
    DATABASE_USER: str = os.getenv("DATABASE_USER", "your_default_db_user")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "your_default_db_password")
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: int = int(os.getenv("DATABASE_PORT", 5432))
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "pharma_inventory")
    
    SQLALCHEMY_DATABASE_URI: str = (
        f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    )

    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_default_secret_key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # Additional settings (e.g., email, third-party services)
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.example.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 587))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "user@example.com")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "email_password")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "noreply@example.com")

    # OAuth2 settings for third-party authentication (if needed)
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    FACEBOOK_CLIENT_ID: str = os.getenv("FACEBOOK_CLIENT_ID", "")
    FACEBOOK_CLIENT_SECRET: str = os.getenv("FACEBOOK_CLIENT_SECRET", "")

    class Config:
        case_sensitive = True

settings = Settings()
