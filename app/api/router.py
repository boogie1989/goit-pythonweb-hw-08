"""
Main API router that includes all endpoint routers.
"""
from fastapi import APIRouter
from app.api.endpoints import contacts

api_router = APIRouter()

# Include all API endpoints
api_router.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
