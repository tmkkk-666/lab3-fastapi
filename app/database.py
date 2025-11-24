from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get database connection details from environment variables
DB_USER = os.getenv("DB_USER", "postgres")  # Default to 'postgres'
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")  # Default to 'postgres'
DB_NAME = os.getenv("DB_NAME", "students_db")  # Default to 'students_db'
DB_HOST = os.getenv("DB_HOST", "localhost")  # Use localhost for local environment
DB_PORT = os.getenv("DB_PORT", "5432")  # Default PostgreSQL port

# Construct database connection URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Debug information
print(f"Attempting to connect to database: {DATABASE_URL}")

# Create database engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Enable connection health checking
    echo=True  # Enable SQL logging during development
)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for ORM models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Ensure session is closed after use