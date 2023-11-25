from aiogram import Bot
from aiogram.types import CallbackQuery

from core.others.db_request import Request


async def answer_reverse(call: CallbackQuery, request: Request, bot: Bot):
    type_answer = call.data.split('=')[0]
    date_answer = call.data.split('=')[1].split('|')[0]
    time_answer = call.data.split('=')[1].split('|')[1]
    id_user_answer = call.data.split('=')[1].split('|')[2]

    text = call.message.text.replace("TASDIQLASHNI KUTMOQDA", '')
    if 'confirmreserve' in type_answer:
        await request.db_change_status('busy', date_answer, time_answer)
        msg_user = f"BUYURTMANGIZ QABUL QILINDI\r\n{text}"
        msg_admin = f"BUYURTMANI QABUL QILDINGIZ\r\n{text}"
    else:
        # await request.db_change_status('busy', date_answer, time_answer)
        msg_user = f"BUYURTMANGIZ QABUL QILINMADI\r\n{text}"
        msg_admin = f"BUYURTMANI QABUL QILMADINGIZ\r\n{text}"

    await call.message.edit_text(msg_admin, reply_markup=None)
    await bot.send_message(id_user_answer, msg_user)
