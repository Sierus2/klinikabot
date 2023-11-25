import re

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from core import settings
from core.keyboards.admin_keyboard import admin_button
from core.keyboards.edit_keyboards import delete_button, buy_button
from core.keyboards.service_button import kb_get_services, kb_get_add_services
from core.keyboards.text_button import get_button_name
from core.keyboards.user_buttons import kb_get_date, kb_get_time, get_contact
from core.others.data_for_users import get_data_state, get_data_for_admin
from core.others.db_request import Request
from core.others.state_user import States


async def handle_add_services(call: CallbackQuery, state: FSMContext):
    print(14)
    add = []
    data = await state.get_data()

    if 'add_serv' in data:
        add = data['add_serv']

    add_service = call.data.split('=')[1].split('|')[0]
    add_service_price = call.data.split('=')[1].split('|')[1]

    add.append({add_service: add_service_price})
    await state.update_data(add_serv=add)
    keyboard = await delete_button(call.message.reply_markup, call.data)
    await call.message.edit_text(await get_data_state(state), reply_markup=keyboard)


async def get_add_service(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    print(31)
    date_needed = data["date"]
    time_needed = data["time"]
    service = call.data.split('=')[1].split('|')[0]
    price = call.data.split('=')[1].split('|')[1]
    await state.update_data(service=service, price=price)
    await state.set_state(States.state_add_service)

    await call.message.edit_text(f"Tanlangan kun: <b>{date_needed}</b>\r\n"
                                 f"Tanlangan vaqt: <b>{time_needed}</b>\r\n"
                                 f"Tanlangan xizmat: <b>{service}</b> - <b>{price}</b>\r\n"
                                 f"Qo'shimcha xizmatlarni tanlashingiz mumkin: ",
                                 reply_markup=await kb_get_add_services())


async def get_service(call: CallbackQuery, state: FSMContext, request: Request):
    data = await state.get_data()
    date_needed = data['date']
    time_needed = call.data.split('=')[1]
    await state.update_data(time=time_needed)
    await state.set_state(States.state_service)

    await call.message.edit_text(f"Tanlangan kun: <b>{date_needed}</b>\r\n"
                                 f"Tanlangan vaqt: <b>{time_needed}</b>\r\n"
                                 f"Endi xizmatni tanlang: ", reply_markup=await kb_get_services())
    await request.db_change_status('process', date_needed, time_needed)


async def get_time(call: CallbackQuery, state: FSMContext, request: Request):
    data_needed = call.data.split('=')[1]

    await call.message.edit_text(f"Tanlangan kun: <b>{data_needed}</b>\r\n Endi soatini tanlang.!",
                                 reply_markup=await kb_get_time(request, data_needed))
    await state.set_state(States.state_time)
    await state.update_data(date=data_needed)


async def get_date(message: Message, state: FSMContext, request: Request):
    await message.answer(f"Tanishganimdan xursandman <b>{message.text}</b>!", reply_markup=await kb_get_date(request))
    await state.update_data(name=message.text)
    await state.set_state(States.state_date)


async def get_name(message: Message, state: FSMContext, request: Request):
    await message.answer("Salom, men Medanta klinikasi onlayn qabul botiman. Sizga kim deb murojaat etsam bo'ladi?",
                         reply_markup=await get_button_name(message.from_user.first_name))
    await state.set_state(States.state_name)
    await request.add_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name,
                           message.from_user.username)


async def application(call: CallbackQuery, state: FSMContext, bot: Bot):
    # await call.message.edit_text(
    #     "Rahmat, buyurtmangiz qabul qilindi. Iltimos telefon raqamingizni qoldiring....\r\n\r\n<em> Namuna: +998901234567</em>",
    #     reply_markup=await get_contact())
    await call.message.delete()
    await bot.send_message(call.message.chat.id, f"Buyurtmangiz qabul qilindi! Endi raqamingizni jo'nating!",
                           reply_markup=ReplyKeyboardMarkup(
                               keyboard=
                               [
                                   [
                                       KeyboardButton(
                                           text="Kontaktni jo'nating",
                                           request_contact=True
                                       )
                                   ]
                               ], resize_keyboard=True, one_time_keyboard=True
                           ))
    await state.set_state(States.state_get_phone)


async def check_phone(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(phone=message.contact.phone_number)

    await message.answer(
        "Buyurtmangiz uchun tashakkur! Menejerlarimiz sizning raqamingizga qo'ng'iroq qilishni boshlashdi. Qo'ng'iroqni kuting..", reply_markup=None)
    data = await state.get_data()
    date_needed = data['date']
    time_needed = data['time']

    await bot.send_message(chat_id=6196151532, text=await get_data_for_admin(state),
                           reply_markup=await admin_button(date=date_needed, time=time_needed,
                                                           user_id=message.from_user.id))
    await state.clear()


async def add_service_cancel(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(await get_data_state(state), reply_markup=await buy_button())


async def clear_cart(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(
        f" <b>Siz savatchani bo'shatdingiz😢</b>\r\n\r\n♻️ <b><em>Agarda qaytadan xarid qilish xoxishi uyg'onsa, </em></b>/start <b><em>tugmasini bosing</em></b>",
        reply_markup=None)


async def check_phone_fake(message: Message):
    await message.answer("Бу сизнинг контагингиз эмас, илтимос текшириб қайта жўнатинг!")