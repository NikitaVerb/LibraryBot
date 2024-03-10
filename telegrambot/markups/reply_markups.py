from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_catalog_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="📚Каталог")
    kb.button(text="❤️Избранное")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
