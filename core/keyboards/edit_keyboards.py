from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def delete_button(keyboard: InlineKeyboardMarkup, el_del):
    keyboard_new = []

    for keys in keyboard.inline_keyboard:
        time_key = []

        for key in keys:
            if el_del not in key.callback_data:
                if 'Rahmat, yetarli' in key.text:
                    key.text = 'Pojaluy xvatit'
                time_key.append(key)

        keyboard_new.append(time_key)
    keyboards = InlineKeyboardMarkup(inline_keyboard=keyboard_new)

    if len(keyboards.inline_keyboard[0]) >= 1:
        return keyboards
    else:
        return await buy_button()


async def buy_button():
    keyboards = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Буюртмани якунлаш!',
                callback_data='application'

            ),
            InlineKeyboardButton(
                text='Тўловга ўтиш!',
                callback_data='order'

            ),
        ],
        [
            InlineKeyboardButton(
                text='Savatchani tozalash',
                callback_data='clean_cart'

            )
        ]
    ])

    return keyboards
