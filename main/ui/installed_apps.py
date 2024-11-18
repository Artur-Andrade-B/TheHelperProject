from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox
from PySide6.QtCore import QStringListModel
from main.utils.registry import list_installed_apps


class InstalledAppsDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Installed Apps")

        # List of installed applications
        self.apps_list = list_installed_apps()

        # Create ComboBox to display apps
        self.combo_box = QComboBox(self)
        self.combo_box.addItems(self.apps_list)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Installed Applications"))
        layout.addWidget(self.combo_box)

        self.resize(300, 150)


class InstalledAppsListModel(QStringListModel):
    def __init__(self, data):
        super().__init__(data)
