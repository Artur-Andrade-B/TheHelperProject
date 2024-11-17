import sys
from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMenu, QDialog
from print_window import PrintWindow

class DraggableWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window to stay on top
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)

        # Make the widget frameless
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # Create a label to show some text
        self.label = QLabel("Drag me around!", self)

        # Create a button to trigger the radial menu
        self.open_menu_button = QPushButton("Open Radial Menu", self)
        self.open_menu_button.clicked.connect(self.open_radial_menu)

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.open_menu_button)

        # Set the widget's initial size
        self.resize(200, 150)

        # Variables for dragging
        self.dragging = False
        self.drag_position = QPoint()

    def mousePressEvent(self, event):
        # Start dragging when mouse is pressed
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        # Move the window if it's being dragged
        if self.dragging:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        # Stop dragging when the mouse button is released
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()

    def open_radial_menu(self):
        # Create a simple radial menu (using QMenu for simplicity)
        menu = QMenu(self)

        # Add a "Quit" action to the menu
        quit_action = menu.addAction("Quit")
        quit_action.triggered.connect(self.close)  # Close the application when clicked

        # Add a "Open Big Window" action to the menu
        open_big_window_action = menu.addAction("Open Big Window")
        open_big_window_action.triggered.connect(self.open_big_window)
        open_print_window_action = menu.addAction("Open Print Window")
        open_print_window_action.triggered.connect(self.open_print_window)
        # Display the menu at the position of the button (or anywhere you like)
        menu.exec_(self.open_menu_button.mapToGlobal(self.open_menu_button.rect().bottomLeft()))

    def open_big_window(self):
        # Create and open a simple "big window"
        self.big_window = BigWindow()
        self.big_window.exec()
    def open_print_window(self):
        # Create and show the PrintWindow when the action is triggered
        print_window = PrintWindow()
        print_window.exec()  # This opens the print window as a modal dialog

class BigWindow(QDialog):
    def __init__(self):
        super().__init__()

        # Set a large size for the window
        self.setWindowTitle("Big Window")
        self.resize(600, 400)

        # A simple label inside the big window
        label = QLabel("This is a big window!", self)
        label.setAlignment(Qt.AlignCenter)

        # Set layout
        layout = QVBoxLayout(self)
        layout.addWidget(label)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create and show the draggable widget
    window = DraggableWidget()
    window.show()

    sys.exit(app.exec())
