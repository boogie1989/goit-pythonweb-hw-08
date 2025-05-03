"""
Configuration settings for the application.
"""
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./contacts.db")

# API settings
API_V1_PREFIX = "/api/v1"
PROJECT_NAME = "Contacts API"
