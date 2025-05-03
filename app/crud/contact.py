"""
CRUD operations for contacts.
"""
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, extract

from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate


def create_contact(db: Session, contact: ContactCreate) -> Contact:
    """
    Create a new contact in the database.
    """
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_contacts(db: Session, skip: int = 0, limit: int = 10) -> List[Contact]:
    """
    Get a list of contacts with pagination.
    """
    return db.query(Contact).offset(skip).limit(limit).all()


def get_contact(db: Session, contact_id: int) -> Optional[Contact]:
    """
    Get a single contact by ID.
    """
    return db.query(Contact).filter(Contact.id == contact_id).first()


def update_contact(db: Session, contact_id: int, contact: ContactUpdate) -> Optional[Contact]:
    """
    Update an existing contact.
    """
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int) -> Optional[Contact]:
    """
    Delete a contact from the database.
    """
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact


def search_contacts(db: Session, query: str) -> List[Contact]:
    """
    Search for contacts based on first name, last name, or email.
    """
    return db.query(Contact).filter(
        or_(
            Contact.first_name.ilike(f"%{query}%"),
            Contact.last_name.ilike(f"%{query}%"),
            Contact.email.ilike(f"%{query}%")
        )
    ).all()


def get_upcoming_birthdays(db: Session) -> List[Contact]:
    """
    Get contacts with birthdays in the upcoming week.
    """
    today = datetime.today().date()
    end_date = today + timedelta(days=7)
    
    return db.query(Contact).filter(
        or_(
            (extract("month", Contact.birthday) == today.month) &
            (extract("day", Contact.birthday) >= today.day) &
            (extract("day", Contact.birthday) <= (
                end_date.day if end_date.month == today.month else 31
            )),

            (end_date.month != today.month) &
            (extract("month", Contact.birthday) == end_date.month) &
            (extract("day", Contact.birthday) <= end_date.day)
        )
    ).all()
