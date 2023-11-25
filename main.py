import asyncio
import logging

import psycopg_pool
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ContentType
from aiogram.filters import Command

from core.filters.is_sender_contact import IsSenderContact
from core.handlers.order import order, pre_checkout_query, buy_complete
from core.handlers.admin_operations import answer_reverse
from core.handlers.steps import *
from core.middlewares.db_middlewares import DbSession
from core.others.db_entry import database_entry
from core.others.state_user import States
from core.settings import Bots, Settings, Db, settings
from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def start_bot(bot: Bot):
    await bot.send_message(chat_id=settings.bots.admin_id, text='Bot is started!')


async def stop_bot(bot: Bot):
    await bot.send_message(chat_id=settings.bots.admin_id, text='Bot is stoped!')


def create_pool(user, host, password, db):
    return psycopg_pool.AsyncConnectionPool(
        f"host={host} port=5432 dbname={db} user={user} password={password} connect_timeout=10"
    )


async def run_bot():
    logging.basicConfig(
        level=logging.INFO
    )
    bot = Bot(settings.bots.bot_token, parse_mode="HTML")
    dp = Dispatcher()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.middleware(
        DbSession(create_pool(settings.db.user, settings.db.host, settings.db.password, settings.db.db)))
    dp.callback_query.middleware(
        DbSession(create_pool(settings.db.user, settings.db.host, settings.db.password, settings.db.db)))

    dp.message.register(buy_complete, F.content_type == ContentType.SUCCESSFUL_PAYMENT)
    dp.pre_checkout_query.register(pre_checkout_query)
    dp.callback_query.register(add_service_cancel, F.data == 'add_service_cancel')
    dp.callback_query.register(order, F.data == 'order')
    dp.callback_query.register(clear_cart, F.data == 'clean_cart')
    dp.callback_query.register(answer_reverse, F.data.regexp(r'confirmreserve*') | F.data.regexp(r'cancelserve*'))
    dp.callback_query.register(application, F.data == 'application')
    dp.message.register(check_phone, States.state_get_phone, IsSenderContact())
    dp.message.register(check_phone_fake, States.state_get_phone)

    dp.callback_query.register(handle_add_services, States.state_add_service)
    dp.callback_query.register(get_add_service, States.state_service)
    dp.callback_query.register(get_service, States.state_time)
    dp.callback_query.register(get_time, States.state_date)

    dp.message.register(get_date, States.state_name)
    dp.message.register(get_name, Command(commands='start'))

    await database_entry()
    schedular = AsyncIOScheduler(timezone='Asia/Tashkent')
    schedular.add_job(database_entry, 'cron', hour=11, minute=25, start_date='2023-11-23 09:00:00')
    schedular.start()

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(run_bot())
    except(KeyboardInterrupt, SystemExit):
        print('Error')
