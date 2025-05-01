from typing import List, Any
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import or_, func

from src.database.models import Contact
from src.schemas.contacts import ContactCreateModel, ContactUpdateModel


class ContactsRepository:

    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_all(
        self,
        birthdays_within: int | None = None,
        search: str | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ):

        stmt = select(Contact).limit(limit).offset(offset)

        if search is not None:
            stmt = stmt.filter(
                or_(
                    Contact.first_name.ilike(f"%{search}%"),
                    Contact.last_name.ilike(f"%{search}%"),
                    Contact.email.ilike(f"%{search}%"),
                )
            )

        if birthdays_within is not None:
            today = datetime.now().date()
            week = today + timedelta(days=birthdays_within)

            stmt = stmt.filter(
                or_(
                    func.to_char(Contact.birthday, "MM-DD").between(
                        today.strftime("%m-%d"), week.strftime("%m-%d")
                    )
                )
            )

        contacts = await self.db.execute(stmt)

        return contacts.scalars().all()

    async def get_one_or_none(
        self,
        filters: List[Any] | None = None,
        order_by: Any = "id",
    ):
        return (
            await self.db.execute(select(Contact).filter(*filters).order_by(order_by))
        ).scalar_one_or_none()

    async def create(self, body: ContactCreateModel):
        contact = Contact(**body.model_dump())
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def update(self, contact_id: int, body: ContactUpdateModel):
        contact = await self.get_one_or_none(filters=[Contact.id == contact_id])

        if contact is None:
            return None

        for key, value in body.model_dump(exclude_unset=True).items():
            setattr(contact, key, value)

        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def delete(self, contact: Contact):
        await self.db.delete(contact)
        await self.db.commit()
        return contact
