from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsSenderContact(BaseFilter):
    is_contact: bool

    async def __call__(self, message: Message) -> bool:
        try:
            self.is_contact = message.contact.user_id == message.from_user.id
        except:
            self.is_contact = False

        return self.is_contact
