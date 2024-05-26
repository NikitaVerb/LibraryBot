import sqlite3

from aiogram import Router, F, types
from aiogram.filters import Command
from telegrambot.markups.reply_markups import get_catalog_kb
from telegrambot.markups.inline_markups import *
from aiogram.types import FSInputFile
from difflib import SequenceMatcher

router = Router()


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('''👋Привет, админ!
Я бот-библиотека, ты можешь найти здесь множество разных книг IT тематики.
Ты можешь посмотреть каталог книг, нажав на кнопку 📚Каталог, находящуюся под клавиатурой.
Необязательно хранить все понравившиеся книги на своём устройстве, ты можешь добавить их в ❤️Избранное''',
                         reply_markup=get_catalog_kb())


@router.message(F.text == "📚Каталог")
async def catalog(message: types.Message):
    await message.answer_photo(caption="Выберите тему",
                               reply_markup=get_catalog_inline_kb(),
                               photo="AgACAgIAAxkBAAIBUGZLGcysvhHKmOBucsW5HaA3KIQiAAKz3TEbsqdZSo7qKEs_6LEqAQADAgADeQADNQQ")


@router.message(F.text == "❤️Избранное")
async def favorite(message: types.Message):
    await message.answer_photo(caption="Избранные книги",
                               photo='AgACAgIAAxkBAAIBhmZLPpYGVwjRstbYxpLq85G4bArcAAKW3jEbsqdZSmqegg673b-3AQADAgADeQADNQQ',
                               reply_markup=get_favorite_book_inline_kb())


@router.callback_query(F.data.startswith("$type$_"))
async def books(callback: types.CallbackQuery):
    book_type = callback.data.split("_", 1)[1]
    await callback.answer()
    await callback.message.answer_photo(
        photo="AgACAgIAAxkBAAIBSmZLF460EHWQMhfw0CZ1DDYehckNAAKs3TEbsqdZSk9B4ovigr1jAQADAgADeQADNQQ",
        caption="Вот книги данного типа",
        reply_markup=get_book_inline_kb(book_type))


@router.callback_query(F.data.startswith("$load$_"))
async def send_book(callback: types.CallbackQuery):
    await callback.answer()
    book_name = callback.data.split("_", 1)[1]
    with sqlite3.connect("database.db") as connect:
        connect.row_factory = sqlite3.Row
        cursor = connect.cursor()
        cursor.execute(f"""SELECT id_book FROM Books WHERE book_name LIKE '{book_name}%'""")
        book_id = [res['id_book'] for res in cursor][0]
        cursor.execute(f"""SELECT caption FROM Books WHERE book_name LIKE '{book_name}%'""")
        book_caption = [res['caption'] for res in cursor][0]
        cursor.execute(f"""SELECT id_book FROM Like""")
        there_in_like = book_id in [res['id_book'] for res in cursor]
    if not there_in_like:
        await callback.message.answer_document(book_id, caption=book_caption,
                                               reply_markup=add_to_favorites_inline_kb(book_name))

    else:
        await callback.message.answer_document(book_id, caption=book_caption,
                                               reply_markup=remove_from_favorites_inline_kb(book_name))


@router.callback_query(F.data.startswith("$favorite$_"))
async def add_to_favorite(callback: types.CallbackQuery):
    book_name = callback.data.split("_", 1)[1]

    with sqlite3.connect("database.db") as connect:
        connect.row_factory = sqlite3.Row
        cursor = connect.cursor()

        # Проверяем, есть ли уже запись для данного пользователя и книги
        cursor.execute(f"""SELECT * FROM Like WHERE user_id = {callback.from_user.id} AND id_book = (
            SELECT id_book FROM Books WHERE book_name LIKE '{book_name}%')""")
        existing_record = cursor.fetchone()

        if existing_record:
            await callback.answer()
            await callback.message.answer("Книга уже добавлена в избранное")
        else:
            # Если записи нет, добавляем книгу в избранное
            cursor.execute(f"""INSERT INTO Like (user_id, id_book) 
                                SELECT {callback.from_user.id}, id_book FROM Books WHERE book_name LIKE '{book_name}%'""")
            await callback.answer()
            await callback.message.answer("Книга добавлена в избранное")


@router.callback_query(F.data.startswith("$delete$_"))
async def delete_from_favorite(callback: types.CallbackQuery):
    book_name = callback.data.split("_", 1)[1]
    with sqlite3.connect("database.db") as connect:
        connect.row_factory = sqlite3.Row
        cursor = connect.cursor()
        cursor.execute(
            f"""DELETE FROM Like WHERE id_book IN (SELECT id_book FROM Books WHERE book_name LIKE '{book_name}%')""")
    await callback.answer()
    await callback.message.answer("Книга удалена из избранного")


@router.message(F.text)
async def search_book(message: types.Message):
    book_name1 = message.text
    with sqlite3.connect("database.db") as connect:
        connect.row_factory = sqlite3.Row
        cursor = connect.cursor()

        cursor.execute("""SELECT id_book FROM "Like" """)
        ids_book = [res['id_book'] for res in cursor]

        cursor.execute("""SELECT id_book, book_name, caption FROM Books""")

        for res in cursor:
            matcher = SequenceMatcher(None, res['book_name'].lower(), book_name1.lower())
            similarity = matcher.ratio()

            if similarity > 0.4:
                await message.answer("Возможно вы имели ввиду эту книгу")
                if res['id_book'] in ids_book:
                    await message.answer_document(res['id_book'], caption=res['caption'],
                                                  reply_markup=remove_from_favorites_inline_kb(res['book_name']))
                else:
                    await message.answer_document(res['id_book'], caption=res['caption'],
                                                  reply_markup=add_to_favorites_inline_kb(res['book_name']))
                break
        else:
            await message.answer("Извините, такой книги не было найдено в нашем каталоге")
