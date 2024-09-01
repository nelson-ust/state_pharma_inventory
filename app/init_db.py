# init_db.py

import os
import sys

# Add the project root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app.db.base import Base  # Import the Base class that holds the metadata for the models
from app.core.config import settings


def database_exists(connection, database_name):
    """
    Check if the given database exists.
    """
    result = connection.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{database_name}';"))
    return result.scalar() is not None

def create_database():
    """
    Create the PostgreSQL database.
    """
    # Connect to the default database 'postgres' to perform admin tasks
    conn = connect(
        dbname='postgres',
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    try:
        # Terminate connections to the database and drop it if it exists
        cursor.execute(f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{settings.DATABASE_NAME}';")
        cursor.execute(f"DROP DATABASE IF EXISTS {settings.DATABASE_NAME};")
        # Create the new database
        cursor.execute(f"CREATE DATABASE {settings.DATABASE_NAME};")
        print(f"Database {settings.DATABASE_NAME} created successfully.")
    finally:
        cursor.close()
        conn.close()

def list_tables(engine):
    """
    List all tables in the database.
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public';"))
        tables = result.fetchall()
        print("Tables in the database:")
        for table in tables:
            print(table[0])

def init_db():
    """
    Initializes the database by checking if it exists, dropping it if it does,
    and then creating it and all associated tables.
    """
    # Connect to the default 'postgres' database to check if the target database exists
    engine = create_engine(f"postgresql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/postgres")
    with engine.connect() as connection:
        if database_exists(connection, settings.DATABASE_NAME):
            print(f"Database {settings.DATABASE_NAME} exists, dropping and recreating it.")
            create_database()
        else:
            print(f"Database {settings.DATABASE_NAME} does not exist, creating it.")
            create_database()

    # Now connect to the newly created database and create all tables
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

    # List the tables in the database
    list_tables(engine)

if __name__ == "__main__":
    init_db()