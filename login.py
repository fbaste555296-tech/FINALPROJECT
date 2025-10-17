from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QInputDialog, QMessageBox
from styles import button_style, MAIN_COLOR, LIGHT_BG
from db import DB_FILE
import sqlite3
from user_dashboard import UserWindow
from admin_dashboard import AdminWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clinic Login")
        self.setFixedSize(300, 250)
        self.setStyleSheet(f"background:{LIGHT_BG};")

        layout = QVBoxLayout()

        title = QLabel("Clinic Appointment System")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color:{MAIN_COLOR};font-size:16px;font-weight:bold;")

        self.user = QLineEdit()
        self.user.setPlaceholderText("Username")

        self.passw = QLineEdit()
        self.passw.setPlaceholderText("Password")
        self.passw.setEchoMode(QLineEdit.Password)

        self.btn_login = QPushButton("Login")
        self.btn_reg = QPushButton("Register")
        for b in (self.btn_login, self.btn_reg):
            b.setStyleSheet(button_style())

        layout.addWidget(title)
        layout.addWidget(self.user)
        layout.addWidget(self.passw)
        layout.addWidget(self.btn_login)
        layout.addWidget(self.btn_reg)

        self.setLayout(layout)

        self.btn_login.clicked.connect(self.login)
        self.btn_reg.clicked.connect(self.register)

    def login(self):
        name, pwd = self.user.text(), self.passw.text()
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("SELECT role FROM users WHERE username=? AND password=?", (name, pwd))
        data = cur.fetchone()
        conn.close()

        if data:
            if data[0] == "Admin":
                self.admin = AdminWindow()
                self.admin.show()
            else:
                self.userwin = UserWindow(name)
                self.userwin.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials.")

    def register(self):
        name, pwd = self.user.text(), self.passw.text()
        if not name or not pwd:
            QMessageBox.warning(self, "Error", "Fields cannot be empty.")
            return
        role, ok = QInputDialog.getItem(self, "Select Role", "Choose role:", ["User", "Admin"], 0, False)
        if ok:
            conn = sqlite3.connect(DB_FILE)
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (name, pwd, role))
                conn.commit()
                QMessageBox.information(self, "Success", "Account created.")
            except sqlite3.IntegrityError:
                QMessageBox.warning(self, "Error", "Username already exists.")
            conn.close()
