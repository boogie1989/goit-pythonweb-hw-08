"""
Pydantic schemas for data validation and serialization.
"""
from app.schemas.contact import ContactBase, ContactCreate, ContactUpdate, ContactInDB

# Export schemas
__all__ = ["ContactBase", "ContactCreate", "ContactUpdate", "ContactInDB"]
