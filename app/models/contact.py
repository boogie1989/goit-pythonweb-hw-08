"""
Contact model definition.
"""
from sqlalchemy import Column, Integer, String, Date
from app.core.database import Base


class Contact(Base):
    """
    Contact database model.
    """
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone_number = Column(String(20), nullable=False)
    birthday = Column(Date, nullable=False)
    additional_info = Column(String(255), nullable=True)
