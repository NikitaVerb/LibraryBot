import sqlite3

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_catalog_inline_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    with sqlite3.connect(r"database.db") as connect:
        connect.row_factory = sqlite3.Row
        cursor = connect.cursor()
        cursor.execute("""SELECT DISTINCT type FROM Books""")
        book_types = [res["type"] for res in cursor]

    for type_book in book_types:
        builder.row(InlineKeyboardButton(text=f"{type_book}".upper(), callback_data=f"$type$_{type_book}"))

    builder.adjust(2)
    kb = builder.as_markup()
    return kb


def get_book_inline_kb(type_book: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    with sqlite3.connect(r"database.db") as connect:
        connect.row_factory = sqlite3.Row
        cursor = connect.cursor()
        cursor.execute(f"""SELECT DISTINCT book_name FROM Books
                           WHERE type = '{type_book.strip()}'""")

        books: list[str] = [res["book_name"] for res in cursor]

    for book_name in books:
        builder.row(InlineKeyboardButton(text=f"{book_name.rsplit('.')[0]}", callback_data=f'$load$_{book_name[:20]}'))

    builder.adjust(1)
    kb = builder.as_markup()
    return kb


def add_to_favorites_inline_kb(book_name: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="❤️Добавить в избранное", callback_data=f"$favorite$_{book_name[:20]}"))
    kb = builder.as_markup()
    return kb


def remove_from_favorites_inline_kb(book_name: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="💔Удалить из избранного", callback_data=f"$delete$_{book_name[:20]}"))
    kb = builder.as_markup()
    return kb


def get_favorite_book_inline_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    with sqlite3.connect(r"database.db") as connect:
        connect.row_factory = sqlite3.Row
        cursor = connect.cursor()
        cursor.execute("""SELECT book_name FROM Books JOIN Like ON Books.id_book = Like.id_book;""")
        books: list[str] = [res["book_name"] for res in cursor]
        for book_name in books:
            builder.row(
                InlineKeyboardButton(text=f"{book_name.rsplit('.')[0]}", callback_data=f'$load$_{book_name[:20]}'))

    builder.adjust(1)
    kb = builder.as_markup()
    return kb
