from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, Message

from core.others.db_request import Request
from core.others.get_data_text import dict_line
from core.settings import settings


async def buy_complete(message: Message, state: FSMContext, bot: Bot, request: Request):
    msg = f"To'lovingiz uchun tashakkur!\r\n\r\nSumma: {message.successful_payment.total_amount // 100} {message.successful_payment.currency}"
    await message.answer(msg)

    data = await state.get_data()

    await request.db_change_status('busy', data['date'], data['time'])
    await state.clear()


async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, state: FSMContext, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    print(pre_checkout_query)

    text = (f"👤 <b>To'lovchi:</b> {pre_checkout_query.from_user.first_name}\r\n"
            f"📞 <b>Telefon raqami:</b> {pre_checkout_query.order_info.phone_number}\r\n"
            f"💴 <b>Summa:</b> {pre_checkout_query.total_amount / 100}")
    # await bot.send_message(settings.bots.admin_id, text=dict_line(dict(pre_checkout_query)))
    await bot.send_message(settings.bots.admin_id, text=text)


async def order(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    service = data['service']
    price = data['price']
    price = data['price']
    labeled_price = [LabeledPrice(
        label=service,
        amount=int(price) * 100
    )]

    if 'add_serv' in data:
        dict_data = data['add_serv']

        for el_data in dict_data:
            for key, value in el_data.items():
                labeled_price.append(
                    LabeledPrice(
                        label=key,
                        amount=int(value) * 100
                    )
                )

    title = "Medanta электрон карта учун тўлов"
    description = "Электрон карта очиш ва хизматлардан фойдаланиш учун онлайн тўлов"
    await bot.send_invoice(
        call.message.chat.id,
        title=title,
        description=description,
        payload='telegram_order',
        provider_token="398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065",
        currency='uzs',
        prices=labeled_price,
        # max_tip_amount=None,
        need_name=True,
        need_phone_number=True,

    )
