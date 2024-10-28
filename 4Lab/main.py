import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableView, QLineEdit, QPushButton,
    QVBoxLayout, QWidget, QHBoxLayout, QMessageBox, QInputDialog
)
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel

class DatabaseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Database Application")
        self.setGeometry(100, 100, 800, 600)

        folder_path = "database_folder"
        db_path = os.path.join(folder_path, "posts.db")

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(db_path)
        if not self.db.open():
            QMessageBox.critical(None, "Database Error", self.db.lastError().text())
            sys.exit(1)

        self.model = QSqlTableModel()
        self.model.setTable("posts")
        self.model.select()

        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Search by title")
        self.search_field.textChanged.connect(self.search_records)

        self.refresh_button = QPushButton("Refresh")
        self.add_button = QPushButton("Add")
        self.delete_button = QPushButton("Delete")

        self.refresh_button.clicked.connect(self.refresh_data)
        self.add_button.clicked.connect(self.add_record)
        self.delete_button.clicked.connect(self.delete_record)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.refresh_button)
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.delete_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.table_view)
        main_layout.addWidget(self.search_field)
        main_layout.addLayout(buttons_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def refresh_data(self):
        self.model.select()

    def search_records(self, text):
        filter_str = f"title LIKE '%{text}%'"
        self.model.setFilter(filter_str)

    def add_record(self):
        user_id, ok_user = QInputDialog.getInt(self, "User ID", "Enter User ID:")
        title, ok_title = QInputDialog.getText(self, "Title", "Enter Title:")
        body, ok_body = QInputDialog.getText(self, "Body", "Enter Body:")

        if ok_user and ok_title and ok_body:
            query = self.model
            row = query.rowCount()
            query.insertRow(row)
            query.setData(query.index(row, 1), user_id)
            query.setData(query.index(row, 2), title)
            query.setData(query.index(row, 3), body)
            query.submitAll()
            self.refresh_data()

    def delete_record(self):
        selected_row = self.table_view.currentIndex().row()
        if selected_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a row to delete.")
            return

        confirm = QMessageBox.question(
            self, "Delete Record", "Are you sure you want to delete this record?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            self.model.removeRow(selected_row)
            self.model.submitAll()
            self.refresh_data()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DatabaseApp()
    window.show()
    sys.exit(app.exec_())
