from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout, QPushButton, QMessageBox
from styles import button_style, MAIN_COLOR, LIGHT_BG
from db import DB_FILE
from dialogs import BookDialog
import sqlite3
from PyQt5.QtCore import Qt

class UserWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("User Dashboard")
        self.setFixedSize(600, 400)
        self.setStyleSheet(f"background:{LIGHT_BG};")

        layout = QVBoxLayout()

        title = QLabel(f"Welcome, {username}")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color:{MAIN_COLOR};font-weight:bold;font-size:16px;")

        self.table = QTableWidget()
        self.table.setStyleSheet("background:#f2f2f2; color:#000;")
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Doctor", "Date", "Time", "Status", "Payment"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        top_buttons = QHBoxLayout()
        self.btn_book = QPushButton("Book Appointment")
        self.btn_cancel = QPushButton("Cancel Appointment")
        self.btn_logout = QPushButton("Logout")
        for b in (self.btn_book, self.btn_cancel, self.btn_logout):
            b.setStyleSheet(button_style())
        top_buttons.addWidget(self.btn_book)
        top_buttons.addWidget(self.btn_cancel)
        top_buttons.addWidget(self.btn_logout)

        layout.addWidget(title)
        layout.addLayout(top_buttons)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.btn_book.clicked.connect(self.book)
        self.btn_cancel.clicked.connect(self.cancel_selected)
        self.btn_logout.clicked.connect(self.close)

        self.table.selectionModel().selectionChanged.connect(self.update_cancel_button)
        self.load_table()
        self.update_cancel_button()

    def load_table(self):
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT id, doctor, date, time, status, payment FROM appointments WHERE username=?", (self.username,))
        rows = cur.fetchall()
        conn.close()

        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

    def book(self):
        dialog = BookDialog(self)
        if dialog.exec_():
            doctor, date, time = dialog.get_data()
            conn = sqlite3.connect(DB_FILE)
            cur = conn.cursor()
            cur.execute("SELECT id FROM appointments WHERE doctor=? AND date=? AND time=? AND status!='Cancelled'",
                        (doctor, date, time))
            if cur.fetchone():
                QMessageBox.warning(self, "Error", "This time slot is already booked.")
            else:
                cur.execute("INSERT INTO appointments (username, doctor, date, time) VALUES (?, ?, ?, ?)",
                            (self.username, doctor, date, time))
                conn.commit()
                QMessageBox.information(self, "Booked", "Appointment booked successfully.")
            conn.close()
            self.load_table()
            self.update_cancel_button()

    def cancel_selected(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "Select an appointment to cancel.")
            return
        aid = int(self.table.item(row, 0).text())
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("UPDATE appointments SET status='Cancelled' WHERE id=? AND username=?", (aid, self.username))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Cancelled", "Appointment cancelled.")
        self.load_table()
        self.update_cancel_button()

    def update_cancel_button(self):
        selected = self.table.currentRow() != -1
        self.btn_cancel.setEnabled(selected)
