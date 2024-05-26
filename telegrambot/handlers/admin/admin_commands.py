from aiogram import Router, F, types
from aiogram.filters import Command
from telegrambot.markups.reply_markups import get_catalog_kb
from telegrambot.filters import user_rights
from aiogram.enums.content_type import ContentType
import sqlite3

router = Router()
router.message.filter(user_rights.UserRightFilter())


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('''👋Привет, админ!
Я бот-библиотека, ты можешь найти здесь множество разных книг IT тематики.
Ты можешь посмотреть каталог книг, нажав на кнопку 📚Каталог, находящуюся под клавиатурой.
Необязательно хранить все понравившиеся книги на своём устройстве, ты можешь добавить их в ❤️Избранное''',
                         reply_markup=get_catalog_kb())


@router.message(F.content_type == ContentType.DOCUMENT)
async def load_doc(message: types.Message):
    book_id = message.document.file_id
    book_name = message.document.file_name
    book_type, book_caption = message.caption.split('\n', 1)

    if book_type is None:
        await message.answer(
            "Не указана категоря, к которой можно отнести книгк, например: C++, SQL, Computer Science и т.п.")
    else:
        with sqlite3.connect("database.db") as connect:
            connect.row_factory = sqlite3.Row
            cursor = connect.cursor()
            cursor.execute(
                f"""INSERT INTO Books (id_book, book_name, type, caption) VALUES ('{book_id}', '{book_name}', '{book_type}', '{book_caption}');""")


@router.message(F.photo)
async def get_photo_id(message: types.Message):
    await message.answer(message.photo[-1].file_id)
