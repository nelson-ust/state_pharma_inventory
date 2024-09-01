from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints.users import router as user_router
from app.core.config import settings
from app.db.session import SessionLocal, engine
from sqlalchemy.orm import Session
import logging
import uvicorn

# Create an instance of the FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production, e.g., ["https://yourdomain.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the user router
app.include_router(user_router, prefix="/api/v1", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Pharmaceutical Inventory System"}

# Event handler for startup
@app.on_event("startup")
async def startup_event():
    # Startup event logic
    logging.info("Starting up the application...")
    
    # Example: Initialize a database connection pool
    try:
        # Preload database session (test connection)
        db: Session = SessionLocal()
        db.execute("SELECT 1")
        logging.info("Database connection established.")
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
    finally:
        db.close()

    # Example: Initialize other resources
    logging.info("Initialization complete.")

# Event handler for shutdown
@app.on_event("shutdown")
async def shutdown_event():
    # Shutdown event logic
    logging.info("Shutting down the application...")
    
    # Example: Clean up or close the database connection pool
    try:
        engine.dispose()
        logging.info("Database connection pool disposed.")
    except Exception as e:
        logging.error(f"Failed to dispose database connection pool: {e}")

    # Example: Clean up other resources
    logging.info("Cleanup complete.")

if __name__ == "__main__":
    logging.info("Starting Uvicorn server...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

