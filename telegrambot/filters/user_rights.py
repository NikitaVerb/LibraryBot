from aiogram.filters import BaseFilter
from aiogram.types import Message
import sqlite3 as sq


class UserRightFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        with sq.connect('database.db') as con:
            con.row_factory = sq.Row
            cursor = con.cursor()
            cursor.execute(f'''SELECT * FROM Admins''')
            admins_id = []
            for res in cursor:
                admins_id.append(res['admin_id'])

        return message.from_user.id in admins_id
