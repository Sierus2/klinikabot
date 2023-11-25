from datetime import datetime
import datetime


class Request:
    def __init__(self, conn):
        self.conn = conn

    async def db_get_time(self, data_needed):
        data_now = datetime.datetime.today()
        # query = f"SELECT DISTINCT b_time FROM booking WHERE b_status = 'free' AND b_date = '{data_needed}' AND b_datetime > '{data_now}' ORDER BY b_time ASC"
        query = f"SELECT DISTINCT b_time, b_status FROM booking WHERE b_date = '{data_needed}' AND b_datetime > '{data_now}' ORDER BY b_time ASC"
        # print(query)
        rows = await self.conn.execute(query)
        results = await rows.fetchall()

        # list_time = [str(result[0].strftime("%H:%M")) for result in results]
        # print(18, list_time)

        return results

    async def db_get_date(self):
        date_now = datetime.datetime.today().strftime("%Y.%m.%d %H:%M:%S")
        query = (
            f"SELECT DISTINCT b_date FROM booking WHERE b_status='free' AND b_datetime > '{date_now}' ORDER BY "
            f"b_date ASC LIMIT 3")
        # print(query)
        rows = await self.conn.execute(query)
        results = await rows.fetchall()

        list_date = [str(result[0].strftime("%Y-%m-%d")) for result in results]
        # print(list_date)
        return list_date

    async def add_user(self, id_user, first_name, last_name, username):
        query = f"INSERT INTO users (telegram_id, first_name, last_name, username) VALUES ('{id_user}','{first_name}','{last_name}','{username}') ON CONFLICT (telegram_id) DO UPDATE SET first_name='{first_name}', last_name='{last_name}', username='{username}'"

        await self.conn.execute(query)

    async def db_change_status(self, status, date, time):
        query = f"UPDATE booking SET b_status='{status}' WHERE b_date='{date}' AND b_time='{time}'"
        await self.conn.execute(query)
