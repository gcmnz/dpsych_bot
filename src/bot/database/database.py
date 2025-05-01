import asyncio

import aiosqlite
from typing import Optional, Iterable


class Database:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.connection: Optional[aiosqlite.Connection] = None

    async def init(self) -> None:
        self.connection = await aiosqlite.connect(self.db_path)
        await self.create_user_table()

    async def close(self) -> None:
        if self.connection:
            await self.connection.close()

    async def create_user_table(self) -> None:
        query = """
        CREATE TABLE IF NOT EXISTS Users (
            tg_user_id INTEGER,
            tg_username TEXT,
            Фамилия TEXT,
            Имя TEXT,
            Файлов_сгенерировано INTEGER,
            Админ BOOLEAN
        )
        """
        await self.connection.execute(query)
        await self.connection.commit()

    async def delete_user(self, tg_user_id: int) -> None:
        query = "DELETE FROM users WHERE tg_user_id = ?"
        await self.connection.execute(query, (tg_user_id,))
        await self.connection.commit()

    async def register_user(self, tg_user_id: int, tg_username: str, is_admin: bool = False) -> bool:
        check_query = "SELECT 1 FROM users WHERE tg_user_id = ?"
        cursor = await self.connection.execute(check_query, (tg_user_id,))
        user_exists = await cursor.fetchone()

        if user_exists:
            return False

        query = """
        INSERT INTO users (tg_user_id, tg_username, Фамилия, Имя, Файлов_сгенерировано, Админ) VALUES (?, ?, ?, ?, ?, ?)
        """
        await self.connection.execute(query, (tg_user_id, f'@{tg_username}', None, None, 0, is_admin))
        await self.connection.commit()

        return True

    async def increment_generate_file(self, tg_user_id: int) -> None:
        query = """
            UPDATE Users
            SET Файлов_сгенерировано = Файлов_сгенерировано + 1
            WHERE tg_user_id = ?
            """
        # Выполнение запроса с использованием подготовленного выражения
        await self.connection.execute(query, (tg_user_id,))
        await self.connection.commit()

    async def is_user_registered(self, tg_user_id: int) -> bool:
        check_query = "SELECT 1 FROM users WHERE tg_user_id = ?"
        cursor = await self.connection.execute(check_query, (tg_user_id,))
        user_exists = await cursor.fetchone()

        return bool(user_exists)

    async def is_user_has_name(self, tg_user_id: int) -> bool:
        query = "SELECT Имя FROM Users WHERE tg_user_id = ?"
        result = await self.connection.execute(query, (tg_user_id,))
        row = await result.fetchone()
        return row is not None and row[0]

    async def is_user_has_surname(self, tg_user_id: int) -> bool:
        query = "SELECT Фамилия FROM Users WHERE tg_user_id = ?"
        result = await self.connection.execute(query, (tg_user_id,))
        row = await result.fetchone()
        return row is not None and row[0]

    async def set_user_name(self, tg_user_id: int, name: str) -> None:
        query = """
            UPDATE Users
            SET Имя = ?
            WHERE tg_user_id = ?
            """
        # Выполнение запроса с использованием подготовленного выражения
        await self.connection.execute(query, (name, tg_user_id))
        await self.connection.commit()

    async def set_user_surname(self, tg_user_id: int, surname: str) -> None:
        query = """
            UPDATE Users
            SET Фамилия = ?
            WHERE tg_user_id = ?
            """
        # Выполнение запроса с использованием подготовленного выражения
        await self.connection.execute(query, (surname, tg_user_id))
        await self.connection.commit()

    async def is_user_admin(self, tg_user_id: int) -> bool:
        query = "SELECT Админ FROM Users WHERE tg_user_id = ?"
        result = await self.connection.execute(query, (tg_user_id,))
        row = await result.fetchone()
        return row is not None and row[0]

    async def get_all_users_id(self) -> list[int]:
        result: list[int] = []

        query = "SELECT * FROM users"
        cursor = await self.connection.execute(query)
        users: Iterable = await cursor.fetchall()
        for user in users:
            print(user)
            tg_user_id: int | None = user[0]
            if tg_user_id is not None:
                result.append(tg_user_id)

        return result

    async def get_user_generated_files(self, tg_user_id: int) -> int:
        query = "SELECT Файлов_сгенерировано FROM Users WHERE tg_user_id = ?"
        result = await self.connection.execute(query, (tg_user_id,))
        row = await result.fetchone()
        return row[0]

    # async def get_user(self, user_id: int) -> Optional[dict]:
    #     query = "SELECT * FROM users WHERE user_id = ?"
    #     cursor = await self.connection.execute(query, (user_id,))
    #     row = await cursor.fetchone()
    #     if row:
    #         return {
    #             "id": row[0],
    #             "user_id": row[1],
    #             "name": row[2],
    #             "date_of_birth": row[3]
    #         }
    #     return None


async def main():
    db = Database("users.db")
    await db.init()
    # print(await db.is_user_registered(tg_username="@O02233"))
    print(await db.get_all_users_id())
    # await db.register_user(tg_user_id=1580689542, tg_username=f"@I84554")
    # Добавление пользователя

    # print(await db.is_user_registered(tg_username="@I84554"))
    #
    # Получение пользователя
    # user = await db.get_user(user_id=12345)
    # print(user)

    # Удаление пользователя
    # await db.delete_user(tg_user_id=12345)

    await db.close()

if __name__ == "__main__":
    asyncio.run(main())
