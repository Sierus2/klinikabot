from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def admin_button(date, time, user_id):
    keyboards = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Tasdiqlash",
                callback_data=f"confirmreserve={date}|{time}|{user_id}"
            ),
            InlineKeyboardButton(
                text="Tasdiqlash",
                callback_data=f"cancelreserve={date}|{time}|{user_id}"
            ),
        ]
    ])
    return keyboards
