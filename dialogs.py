from PyQt5.QtWidgets import QDialog, QFormLayout, QComboBox, QDateEdit, QTimeEdit, QPushButton
from PyQt5.QtCore import QDate, QTime
from styles import button_style, LIGHT_BG

class BookDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Book Appointment")
        self.setFixedSize(300, 200)
        self.setStyleSheet(f"background:{LIGHT_BG};")
        layout = QFormLayout(self)

        self.doctor = QComboBox()
        self.doctor.addItems(["Doctor A", "Doctor B", "Doctor C", "Doctor D"])

        self.date = QDateEdit(QDate.currentDate())
        self.date.setCalendarPopup(True)

        self.time = QTimeEdit(QTime(9, 0))
        self.time.setDisplayFormat("hh:mm AP")

        layout.addRow("Doctor:", self.doctor)
        layout.addRow("Date:", self.date)
        layout.addRow("Time:", self.time)

        btn = QPushButton("Book")
        btn.setStyleSheet(button_style())
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)

    def get_data(self):
        return (
            self.doctor.currentText(),
            self.date.date().toString("yyyy-MM-dd"),
            self.time.time().toString("hh:mm AP")
        )
