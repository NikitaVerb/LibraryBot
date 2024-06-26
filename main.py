import asyncio
import logging
from aiogram import Bot, Dispatcher
from config_reader import config
from telegrambot.handlers.user import user_commands
from telegrambot.handlers.admin import admin_commands


logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode='HTML')
    dp = Dispatcher()
    dp.include_router(admin_commands.router)
    dp.include_router(user_commands.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
