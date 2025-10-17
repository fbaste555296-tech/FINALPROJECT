from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout, QPushButton, QMessageBox
from styles import button_style, LIGHT_BG
from db import DB_FILE
import sqlite3
from PyQt5.QtCore import Qt

class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Dashboard")
        self.setFixedSize(700, 450)
        self.setStyleSheet(f"background:{LIGHT_BG};color:#000;")

        layout = QVBoxLayout()

        title = QLabel("Admin - Appointments")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color:#004d4d;font-weight:bold;font-size:16px;")

        self.table = QTableWidget()
        self.table.setStyleSheet("background:#f2f2f2; color:#000;")
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Username", "Doctor", "Date", "Time", "Status", "Payment"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        top_buttons = QHBoxLayout()
        self.btn_paid = QPushButton("Mark as Paid")
        self.btn_unpaid = QPushButton("Mark as Unpaid")
        self.btn_logout = QPushButton("Logout")
        for b in (self.btn_paid, self.btn_unpaid, self.btn_logout):
            b.setStyleSheet(button_style())
        top_buttons.addWidget(self.btn_paid)
        top_buttons.addWidget(self.btn_unpaid)
        top_buttons.addWidget(self.btn_logout)

        layout.addWidget(title)
        layout.addLayout(top_buttons)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.btn_paid.clicked.connect(lambda: self.update_payment("Paid"))
        self.btn_unpaid.clicked.connect(lambda: self.update_payment("Unpaid"))
        self.btn_logout.clicked.connect(self.close)

        self.table.selectionModel().selectionChanged.connect(self.update_payment_buttons)
        self.load_table()
        self.update_payment_buttons()

    def load_table(self):
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT id, username, doctor, date, time, status, payment FROM appointments ORDER BY date, time")
        rows = cur.fetchall()
        conn.close()

        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
        self.update_payment_buttons()

    def update_payment_buttons(self):
        row = self.table.currentRow()
        if row == -1:
            self.btn_paid.setEnabled(False)
            self.btn_unpaid.setEnabled(False)
        else:
            payment_status = self.table.item(row, 6).text()
            if payment_status == "Unpaid":
                self.btn_paid.setEnabled(True)
                self.btn_unpaid.setEnabled(False)
            elif payment_status == "Paid":
                self.btn_paid.setEnabled(False)
                self.btn_unpaid.setEnabled(True)
            else:
                self.btn_paid.setEnabled(False)
                self.btn_unpaid.setEnabled(False)

    def update_payment(self, status):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "Select an appointment first.")
            return
        aid = int(self.table.item(row, 0).text())
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("UPDATE appointments SET payment=? WHERE id=?", (status, aid))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Updated", f"Appointment #{aid} marked as {status}.")
        self.load_table()
        self.update_payment_buttons()
