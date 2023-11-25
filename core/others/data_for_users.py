from aiogram.fsm.context import FSMContext


async def get_data_state(state: FSMContext):
    data = await state.get_data()
    date_needed = data['date']
    time_needed = data['time']
    service = data['service']
    price = data['price']
    text_user = f"Tanlangan kun: <b>{date_needed}</b>\r\n" \
                f"Tanlangan vaqt: <b>{time_needed}</b>\r\n" \
                f"Tanlangan xizmat: <b>{service}</b> - <b>{price}</b>\r\n"
    total_price = (int(price))

    if 'add_serv' in data:
        dict_data = data['add_serv']
        text_user += f"\r\n Tanlangan xizmatlar: "

        for el_data in dict_data:
            for key, value in el_data.items():
                text_user += f'\r\n <b>🔹{key} {value}$ </b>'
                total_price += int(value)
        text_user += f"\r\n\r\n 💶 Summa: <b>{total_price}</b>"

    return text_user


async def get_data_for_admin(state: FSMContext):
    data = await state.get_data()
    date_needed = data['date']
    time_needed = data['time']
    service = data['service']
    price = data['price']


    name = data['name']
    phone = data['phone']

    text_user = f"❗️<b><em>TASDIQLASHNI KUTMOQDA</em></b>\r\n"\
                 f"Ismi: <b>{name}</b>\r\n " \
                 f"Telefon raqami: <b>{phone}</b>\r\n\r\n " \
                 f"Kun: <b>{date_needed}</b>\r\n" \
                f"Soati: <b>{time_needed}</b>\r\n\r\n\r" \
                f"Tanlangan xizmat: <b>{service}</b> - <b>{price}</b>\r\n"
    total_price = (int(price))

    if 'add_serv' in data:
        dict_data = data['add_serv']
        text_user += f"\r\n Tanlangan xizmatlar: "

        for el_data in dict_data:
            for key, value in el_data.items():
                text_user += f'\r\n <b>🔹{key} {value}$ </b>'
                total_price += int(value)
        text_user += f"\r\n\r\n 💶 Summa: <b>{total_price}</b>"

    return text_user