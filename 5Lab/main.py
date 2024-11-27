from PyQt5 import QtWidgets, QtSql, QtCore
from PyQt5.QtCore import QTimer
import sys
import requests
import asyncio
import sqlite3
import os

os.environ["QT_PLUGIN_PATH"] = r"C:\Users\Арсений\AppData\Local\Programs\Python\Python312\Lib\site-packages\PyQt5\Qt5\plugins"

# Подключение к БД
def create_connection():
    DB = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    DB.setDatabaseName('posts.db')
    if not DB.open():
        QtWidgets.QMessageBox.critical(None, "Ошибка", "Не удалось подключиться к базе данных.")
        return False
    return True

class AddRecordDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить запись")
        self.setFixedSize(300, 200)

        self.postUserID_text = QtWidgets.QLineEdit(self)
        self.postTitle_text = QtWidgets.QLineEdit(self)
        self.postBody_text = QtWidgets.QLineEdit(self)

        self.postUserID_text.setPlaceholderText("UserID")
        self.postTitle_text.setPlaceholderText("Title")
        self.postBody_text.setPlaceholderText("Body")

        self.add_button = QtWidgets.QPushButton("Добавить", self)
        self.cancel_button = QtWidgets.QPushButton("Отмена", self)

        self.add_button.clicked.connect(self.add_record)
        self.cancel_button.clicked.connect(self.reject)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.postUserID_text)
        layout.addWidget(self.postTitle_text)
        layout.addWidget(self.postBody_text)
        layout.addWidget(self.add_button)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

    def add_record(self):
        user_id = self.postUserID_text.text()
        title = self.postTitle_text.text()
        body = self.postBody_text.text()

        row = main_model.rowCount()
        main_model.insertRow(row)
        main_model.setData(main_model.index(row, 1), user_id)
        main_model.setData(main_model.index(row, 2), title)
        main_model.setData(main_model.index(row, 3), body)
        
        if not main_model.submitAll():
            QtWidgets.QMessageBox.warning(None, "Ошибка", "Не удалось добавить запись.")
        else:
            main_model.select()
            self.accept()

        self.clear_fields()

    def clear_fields(self):
        self.postUserID_text.clear()
        self.postTitle_text.clear()
        self.postBody_text.clear()

def delete_record():
    index = main_table.selectionModel().currentIndex()
    if index.isValid():
        main_model.removeRow(index.row())
        if not main_model.submitAll():
            QtWidgets.QMessageBox.warning(None, "Ошибка", "Не удалось удалить запись.")
        else:
            main_model.select()
    else:
        QtWidgets.QMessageBox.warning(None, "Ошибка", "Не Выделена ни одна запись")

def search_post():
    search_text = search_line.text()
    filter_str = f"Title LIKE '%{search_text}%'"
    main_model.setFilter(filter_str)
    main_model.select()

def refresh_table():
    main_model.select()

class UploadData(QtCore.QThread):
    progress_updated = QtCore.pyqtSignal(int)
    upload_finished = QtCore.pyqtSignal()

    def run(self):
        asyncio.run(self.upload_posts())

    async def upload_posts(self):
        await asyncio.sleep(3)
        url = "https://jsonplaceholder.typicode.com/posts"
        allposts = requests.get(url)
        posts = allposts.json()
        await self.clear_table_and_insert(posts)

    async def clear_table_and_insert(self, posts):
        
        rows = main_model.rowCount()
        if rows > 0:
            main_model.removeRows(0, rows)
            main_model.submitAll()

        connection = sqlite3.connect('posts.db')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM posts")
        connection.commit()

        total_posts = len(posts)

        for index, onepost in enumerate(posts):
            await asyncio.sleep(0.1)
            cursor.execute(
                "INSERT INTO posts(user_id, title, body) VALUES (?, ?, ?)",
                (onepost["userId"], onepost["title"], onepost["body"])
            )
            connection.commit()
            self.progress_updated.emit(int((index + 1) / total_posts * 100))

        connection.close()
        self.upload_finished.emit()
        main_model.select()

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()

window.resize(800, 600)

search_line = QtWidgets.QLineEdit()
search_line.setPlaceholderText("Поиск")
main_table = QtWidgets.QTableView()

upload_button = QtWidgets.QPushButton("Загрузить данные")
add_button = QtWidgets.QPushButton("Добавить")
delete_button = QtWidgets.QPushButton("Удалить")
refresh_button = QtWidgets.QPushButton("Обновить")

main_layout = QtWidgets.QVBoxLayout()
button_layout = QtWidgets.QHBoxLayout()

progress_bar = QtWidgets.QProgressBar()

button_layout.addWidget(add_button)
button_layout.addWidget(delete_button)
button_layout.addWidget(refresh_button)

main_layout.addWidget(upload_button)
main_layout.addWidget(progress_bar)
main_layout.addWidget(search_line)
main_layout.addWidget(main_table)
main_layout.addLayout(button_layout)

window.setLayout(main_layout)

connection = create_connection()
main_model = QtSql.QSqlTableModel()
main_model.setTable("posts")
main_model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
main_model.select()

upload_data = UploadData()
upload_data.progress_updated.connect(progress_bar.setValue)

upload_button.clicked.connect(lambda: upload_data.start())
add_button.clicked.connect(lambda: AddRecordDialog().exec_())
delete_button.clicked.connect(delete_record)
refresh_button.clicked.connect(refresh_table)
search_line.textChanged.connect(search_post)

main_table.setModel(main_model)
selection_model = main_table.selectionModel()

refresh_timer = QTimer()
refresh_timer.setInterval(10000)
refresh_timer.timeout.connect(refresh_table)
refresh_timer.start()

window.show()
sys.exit(app.exec())
