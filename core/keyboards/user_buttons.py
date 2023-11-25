from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from core.others.db_request import Request


async def kb_get_time(request: Request, data_needed):
    list_time = await request.db_get_time(data_needed)
    time_list: List[InlineKeyboardButton] = []
    buttons: List = []
    print(12, list_time)
    for el_time in list_time:
        if len(time_list) == 3:
            buttons.append(time_list)
            time_list = []

        button = InlineKeyboardButton(
            text=f"{str(el_time[0])[0:5]}❌" if el_time[1] == 'process' else f"{str(el_time[0])[0:5]}✅",
            # el_tiem_statuse == 'free'
            callback_data=f'reverse_time={el_time[0]}'
        )
        time_list.append(button)

    buttons.append(time_list)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def kb_get_date(request: Request):
    list_date = await request.db_get_date()

    time_list: List[InlineKeyboardButton] = []
    buttons = []

    for el_date in list_date:
        if len(time_list) == 3:
            buttons.append(time_list)
            time_list = []
        button = InlineKeyboardButton(
            text=el_date,
            callback_data=f'reverse_date={el_date}'
        )

        time_list.append(button)
    buttons.append(time_list)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def get_contact():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(
                text="Kontaktni jo'natish",
                request_contact=True,
            )
        ]
    ])
    return kb
