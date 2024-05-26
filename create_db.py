import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# Создаем таблицу Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS Books (
    id_book TEXT PRIMARY KEY,
    book_name TEXT NOT NULL,
    type TEXT NOT NULL,
    caption TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Like (
    user_id INTEGER,
    id_book TEXT NOT NULL,
    PRIMARY KEY(user_id, id_book), 
    FOREIGN KEY(id_book) REFERENCES Books(id_book)
    ON DELETE CASCADE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Admins (
    admin_id INTEGER PRIMARY KEY
)
''')

cursor.execute("""INSERT INTO Admins (admin_id) VALUES (988750689);""")

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()