# main.py
import sys
from PySide6.QtWidgets import QApplication
from draggable_window import DraggableWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = DraggableWidget()
    window.show()

    sys.exit(app.exec())
