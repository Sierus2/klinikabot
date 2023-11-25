from datetime import datetime as dt, timedelta
import datetime
import psycopg
from psycopg import Connection

from core.settings import settings


async def database_entry():
    with psycopg.connect(
            f"host={settings.db.host} port=5432 dbname={settings.db.db} user={settings.db.user} password={settings.db.password} connect_timeout=10") as conn:
        if await get_count_row(conn) < 1:
            query = await get_query(3, str(dt.today().date()))
        else:
            query = await get_query(1, str(dt.today().date()))
        #
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()


async def get_count_row(conn: Connection):
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM booking")
        count = cur.fetchone()
    return count[0]


async def get_query(count_days, target_day):
    query = "INSERT INTO booking (b_date, b_time, b_status, b_datetime) VALUES"  # So'rovni boshi

    target = dt.strptime(target_day, "%Y-%m-%d").date() + datetime.timedelta(
        days=1)  # Qaysi kundan boshlab hisoblash

    for x in range(count_days):
        date_target = target + datetime.timedelta(days=x)  # Bazaga qo'shiladigan kun
        for i in range(0, 10 * 60, 60):
            time_delta = f"{(dt.combine(datetime.date.today(), datetime.time(8, 0)) + timedelta(minutes=i)).time().strftime('%H:%M')}"
            full_date_time = f"{date_target} {time_delta}"
            line = f"\r\n('{date_target}', '{time_delta}', 'free', '{full_date_time}'),"
            query += line

    query = f"{query.rstrip(query[-1])};"
    print(f"{query}")
    return query

# get_query(5, str(dt.today().date()))
