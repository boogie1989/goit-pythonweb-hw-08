"""
Database connection configuration.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL from environment variables, with fallback to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/hw7")
