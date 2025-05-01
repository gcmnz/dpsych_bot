import asyncio

from src.bot.bot import bot, db, dp, send_greet_messages


async def main() -> None:
    await db.init()

    tasks: list[asyncio.Task] = [
        asyncio.create_task(dp.start_polling(bot)),
        asyncio.create_task(send_greet_messages())
    ]

    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
