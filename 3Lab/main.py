import sqlite3
import requests

# Создание базы данных и подключение к ней
conn = sqlite3.connect('posts.db')
cursor = conn.cursor()

# Создание таблицы posts
cursor.execute('''
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    title TEXT,
    body TEXT
)
''')

# Сохранение изменений
conn.commit()

# Получение данных с сервера
url = "https://jsonplaceholder.typicode.com/posts"
response = requests.get(url)

# Преобразование данных в формат JSON
posts_data = response.json()

# Запись данных в базу данных
for post in posts_data:
    cursor.execute('''
    INSERT OR IGNORE INTO posts (id, user_id, title, body) 
    VALUES (?, ?, ?, ?)
    ''', (post['id'], post['userId'], post['title'], post['body']))

# Сохранение изменений в базе данных
conn.commit()

# Функция для получения постов по user_id
def get_posts_by_user(user_id):
    cursor.execute('SELECT * FROM posts WHERE user_id = ?', (user_id,))
    posts = cursor.fetchall()
    return posts

# Пример использования функции
user_id = 1
user_posts = get_posts_by_user(user_id)

# Вывод постов конкретного пользователя
for post in user_posts:
    print(f"ID: {post[0]}, User ID: {post[1]}, Title: {post[2]}, Body: {post[3]}")

# Закрытие соединения с базой данных
conn.close()