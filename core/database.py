import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from dotenv import load_dotenv

# Load environment variables from .env file (optional)
load_dotenv()

# SQLAlchemy Base
Base = declarative_base()

# Environment-specific configurations
ENV = os.getenv("ENV", "development")  # Default to development if ENV is not set 



if ENV == "development":
    # Local PostgreSQL settings
    DB_USER = os.getenv("DEV_DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DEV_DB_PASSWORD", "postgres")
    DB_HOST = os.getenv("DEV_DB_HOST", "0.0.0.0")
    DB_PORT = os.getenv("DEV_DB_PORT", "5432")
    DB_NAME = os.getenv("DEV_DB_NAME", "appdb")

elif ENV == "production":
    # AWS PostgreSQL settings
    DB_USER = os.getenv("PROD_DB_USER")
    DB_PASSWORD = os.getenv("PROD_DB_PASSWORD")
    DB_HOST = os.getenv("PROD_DB_HOST")
    DB_PORT = os.getenv("PROD_DB_PORT")
    DB_NAME = os.getenv("PROD_DB_NAME")

else:
    raise ValueError("Invalid ENV value. Use 'development' or 'production'.")

DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine and session
engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=True,
    future=True
)  # Pre-ping ensures live connection

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency for FastAPI to use DB sessions
async def get_db():
    async with async_session() as db:
        yield db
