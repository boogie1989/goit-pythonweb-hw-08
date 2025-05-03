"""
CRUD (Create, Read, Update, Delete) operations for database interactions.
"""
from app.crud.contact import (
    create_contact, get_contacts, get_contact, update_contact,
    delete_contact, search_contacts, get_upcoming_birthdays
)

# Export CRUD operations
__all__ = [
    "create_contact",
    "get_contacts",
    "get_contact",
    "update_contact",
    "delete_contact",
    "search_contacts",
    "get_upcoming_birthdays"
]
