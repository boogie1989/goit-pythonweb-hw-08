from datetime import date, timedelta
from sqlalchemy import or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.contacts import ContactsRepository
from src.database.models import Contact
from src.schemas.contacts import ContactCreateModel, ContactUpdateModel
from src.utils import HTTPNotFoundException


class ContactsService:
    def __init__(self, db: AsyncSession):
        self.contacts_repository = ContactsRepository(db)

    async def get_all(
        self,
        search: str | None = None,
        birthdays_within: int | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ):

        return await self.contacts_repository.get_all(
            search=search,
            birthdays_within=birthdays_within,
            offset=offset,
            limit=limit,
        )

    async def get_by_id(self, contact_id: int):
        filters = [Contact.id == contact_id]
        contact = await self.contacts_repository.get_one_or_none(filters=filters)

        if contact is None:
            raise HTTPNotFoundException("Not found")

        return contact

    async def create(self, body: ContactCreateModel):
        return await self.contacts_repository.create(body)

    async def update_by_id(self, contact_id: int, body: ContactUpdateModel):
        return await self.contacts_repository.update(contact_id, body)

    async def delete_by_id(self, contact_id: int):
        contact = await self.get_by_id(contact_id)
        return await self.contacts_repository.delete(contact)
