from aiogram import Router, F, types
from aiogram.filters import Command
from telegrambot.markups.reply_markups import get_catalog_kb

router = Router()


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(f'hello, {message.from_user.first_name}', reply_markup=get_catalog_kb())
