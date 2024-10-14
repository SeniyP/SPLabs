import sqlite3
import requests

conn = sqlite3.connect('posts.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    title TEXT,
    body TEXT
)
''')

conn.commit()

url = "https://jsonplaceholder.typicode.com/posts"
response = requests.get(url)

posts_data = response.json()

for post in posts_data:
    cursor.execute('''
    INSERT OR IGNORE INTO posts (id, user_id, title, body) 
    VALUES (?, ?, ?, ?)
    ''', (post['id'], post['userId'], post['title'], post['body']))

conn.commit()

def get_posts_by_user(user_id):
    cursor.execute('SELECT * FROM posts WHERE user_id = ?', (user_id,))
    posts = cursor.fetchall()
    return posts

user_id = 1
user_posts = get_posts_by_user(user_id)

for post in user_posts:
    print(f"ID: {post[0]}, User ID: {post[1]}, Title: {post[2]}, Body: {post[3]}")

conn.close()
