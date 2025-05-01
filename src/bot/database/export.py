import asyncio
import sqlite3
import io

import pandas as pd


async def convert_db_to_excel(db) -> bytes:
    # Create a synchronous connection for pandas operations
    sync_connection = sqlite3.connect(db.db_path)

    # Получение списка всех таблиц в базе данных
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables = pd.read_sql_query(query, sync_connection)

    # Создание объекта BytesIO для записи данных в Excel
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        # Итерация по всем таблицам и запись их в Excel
        for table in tables['name']:
            df = pd.read_sql_query(f"SELECT * FROM {table}", sync_connection)
            df.to_excel(writer, sheet_name=table, index=False)

    # Reset the buffer position to the beginning
    excel_buffer.seek(0)

    # Close the synchronous connection
    sync_connection.close()

    return excel_buffer.read()


async def main():
    from database import Database
    db = Database('users.db')
    await db.init()
    await convert_db_to_excel(db)


if __name__ == '__main__':
    asyncio.run(main())
