from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QMenu, QGraphicsEllipseItem, QGraphicsScene, QGraphicsView

class RadialMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("QMenu { border: none; background: transparent; }")
        self.setAttribute(Qt.WA_OpaquePaintEvent)

        self.setGeometry(100, 100, 300, 300)  # Set default position and size
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.NoDropShadowWindowHint)

        self.items = []
        self.angle_step = 0
        self.center_point = QPoint(self.width() // 2, self.height() // 2)

    def add_item(self, text, action_callback):
        """Add an item to the radial menu."""
        item = RadialMenuItem(self, text, action_callback)
        self.items.append(item)
        self.angle_step += 360 / len(self.items)

    def paintEvent(self, event):
        """Custom paint event to draw the radial menu."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(0, 0, 0, 100))  # Background color
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(self.center_point, self.width() // 2, self.height() // 2)

        for idx, item in enumerate(self.items):
            item.set_position(self.center_point, self.angle_step * idx)
            item.update()

    def open(self):
        """Override the open method to trigger the radial menu."""
        super().open()
        self.repaint()  # Trigger the painting of the radial menu items

    def exec_(self, *args, **kwargs):
        """Override exec_ to keep menu open until user selects an item."""
        super().exec_(*args, **kwargs)


class RadialMenuItem(QGraphicsEllipseItem):
    def __init__(self, menu, text, action_callback):
        super().__init__(0, 0, 100, 100)  # Default size for the item
        self.menu = menu
        self.text = text
        self.action_callback = action_callback
        self.setBrush(QColor(50, 50, 50, 200))  # Item color
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable)

    def set_position(self, center, angle):
        """Set the position of the radial item based on the angle."""
        x = center.x() + (self.menu.width() // 2) * 0.7 * Qt.cos(Qt.radians(angle))
        y = center.y() + (self.menu.height() // 2) * 0.7 * Qt.sin(Qt.radians(angle))
        self.setPos(x - self.rect().width() / 2, y - self.rect().height() / 2)

    def paint(self, painter, option, widget=None):
        """Custom painting of the radial item."""
        painter.setBrush(self.brush())
        painter.setPen(QColor(200, 200, 200))
        painter.drawEllipse(self.rect())
        painter.drawText(self.rect(), Qt.AlignCenter, self.text)

    def mousePressEvent(self, event):
        """Handle item click event to trigger action."""
        self.action_callback()
        self.menu.close()  # Close the radial menu after selection
