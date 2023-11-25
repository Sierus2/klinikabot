from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def get_button_name(name):
    return ReplyKeyboardMarkup(
        keyboard=
        [
            [
                KeyboardButton(
                    text=name
                )
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder='Ismingizni kiriting....',
        one_time_keyboard=True
    )
