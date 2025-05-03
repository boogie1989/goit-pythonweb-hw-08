"""
API endpoints for contact operations.
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.contact import ContactCreate, ContactUpdate, ContactInDB
from app.crud.contact import (
    create_contact, get_contacts, get_contact, update_contact,
    delete_contact, search_contacts, get_upcoming_birthdays
)

router = APIRouter()


@router.post("/", response_model=ContactInDB)
def create_new_contact(contact: ContactCreate, db: Session = Depends(get_db)) -> ContactInDB:
    """
    Create a new contact.
    """
    return create_contact(db, contact)


@router.get("/", response_model=List[ContactInDB])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> List[ContactInDB]:
    """
    Get a list of contacts with pagination.
    """
    return get_contacts(db, skip, limit)


@router.get("/{contact_id}", response_model=ContactInDB)
def read_contact(contact_id: int, db: Session = Depends(get_db)) -> ContactInDB:
    """
    Get a specific contact by ID.
    """
    db_contact = get_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.put("/{contact_id}", response_model=ContactInDB)
def update_existing_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)) -> ContactInDB:
    """
    Update an existing contact.
    """
    db_contact = update_contact(db, contact_id, contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.delete("/{contact_id}", response_model=ContactInDB)
def delete_existing_contact(contact_id: int, db: Session = Depends(get_db)) -> ContactInDB:
    """
    Delete an existing contact.
    """
    db_contact = delete_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


@router.get("/search/", response_model=List[ContactInDB])
def search_contacts_endpoint(query: str = Query(..., min_length=1), db: Session = Depends(get_db)) -> List[ContactInDB]:
    """
    Search for contacts by name or email.
    """
    return search_contacts(db, query)


@router.get("/birthdays/", response_model=List[ContactInDB])
def get_upcoming_birthdays_endpoint(db: Session = Depends(get_db)) -> List[ContactInDB]:
    """
    Get contacts with birthdays in the upcoming week.
    """
    return get_upcoming_birthdays(db)
