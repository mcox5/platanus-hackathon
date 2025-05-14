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
ENV = os.getenv("ENVIRONMENT", "development")  # Check for ENVIRONMENT variable first (used in ECS)

# If ENVIRONMENT not set, try using ENV as fallback
if not ENV:
    ENV = os.getenv("ENV", "development")

print(f"Starting application in {ENV} environment")

if ENV == "development":
    # Local PostgreSQL settings
    DB_USER = os.getenv("DEV_DB_USER", "postgres")
    DB_HOST = os.getenv("DEV_DB_HOST", "localhost")
    DB_PASSWORD = os.getenv("DEV_DB_PASSWORD", "postgres")
    DB_PORT = os.getenv("DEV_DB_PORT", "5432")
    DB_NAME = os.getenv("DEV_DB_NAME", "appdb")
    
    # Use development-specific DATABASE_URL if available
    DATABASE_URL = os.getenv("DEV_DATABASE_URL") or f"postgresql+asyncpg://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    print(f"Development database configured with host: {DB_HOST}, database: {DB_NAME}")

elif ENV == "production":
    # AWS PostgreSQL settings
    DB_USER = os.getenv("PROD_DB_USER", os.getenv("DB_USERNAME"))
    DB_PASSWORD = os.getenv("PROD_DB_PASSWORD", os.getenv("DB_PASSWORD"))
    DB_HOST = os.getenv("PROD_DB_HOST", os.getenv("DB_HOST"))
    DB_PORT = os.getenv("PROD_DB_PORT", "5432")
    DB_NAME = os.getenv("PROD_DB_NAME", os.getenv("DB_NAME", "appdb"))
    
    # Use production-specific DATABASE_URL if available
    DATABASE_URL = os.getenv("PROD_DATABASE_URL") or f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    print(f"Production database configured with host: {DB_HOST}, database: {DB_NAME}")

else:
    raise ValueError(f"Invalid environment value: {ENV}. Use 'development' or 'production'.")


if DATABASE_URL:
    print(f"Database URL created successfully")
else:
    raise ValueError("Failed to create DATABASE_URL")

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
