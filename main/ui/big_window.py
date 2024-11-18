from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

class BigWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Big Window")

        # Label in big window
        self.label = QLabel("This is a big window.", self)
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

        self.setGeometry(100, 100, 600, 400)  # Window size and position
