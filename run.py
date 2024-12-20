import sys
from PySide6.QtWidgets import QApplication
from main.ui.draggable_widget import DraggableWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create and show the draggable widget
    window = DraggableWidget()
    window.show()

    sys.exit(app.exec())
