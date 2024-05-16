import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# Создаем таблицу Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS Books (
    id_book INTEGER PRIMARY KEY,
    book_name TEXT NOT NULL,
    type TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Like (
    user_id INTEGER,
    id_book INTEGER NOT NULL,
    PRIMARY KEY(user_id, id_book), 
    FOREIGN KEY(user_id) REFERENCES Books(id_books)
    ON DELETE CASCADE
)
''')

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()