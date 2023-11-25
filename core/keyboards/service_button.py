from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def kb_get_services():
    dict_service = {
        "Ko'rik": 600,
        "Paximetriya": 500,
        "Excimer Laser": 620,
        "FEK + IOL": 300,
        "Bob": 200,
        "Alif": 650,
        "Lala": 750
    }
    time_list: List[InlineKeyboardButton] = []
    buttons: List = []

    for k, v in dict_service.items():
        if len(time_list) == 2:
            buttons.append(time_list)
            time_list = []
        button = InlineKeyboardButton(
            text=f"{k}-{v}",
            callback_data=f'service={k}|{v}'
        )
        time_list.append(button)

    buttons.append(time_list)
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def kb_get_add_services():
    dict_service = {
        "Sopdrops": 600,
        "Gilan": 500,
        "Xilokeya": 620,
        "Sitramon": 300,

    }
    time_list: List[InlineKeyboardButton] = []
    buttons: List = []
    i = 0
    for k, v in dict_service.items():

        if len(time_list) == 2:
            buttons.append(time_list)
            time_list = []
        button = InlineKeyboardButton(
            text=f"{k}-{v}",
            callback_data=f'service={k}|{v}'
        )

        time_list.append(button)

    buttons.append(time_list)
    button_cancel = InlineKeyboardButton(
        text=f"Rahmat, shart emas!",
        callback_data="add_service_cancel"
    )
    buttons.append([button_cancel])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
