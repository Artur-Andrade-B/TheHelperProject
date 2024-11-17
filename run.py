import sys
import os
import winreg
import subprocess
from PySide6.QtCore import Qt, QPoint, QStandardPaths, QStringListModel, QUrl, QAbstractListModel, QModelIndex
from PySide6.QtGui import QIcon,QPixmap
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMenu, QDialog, QLineEdit, QListView, QHBoxLayout, QListWidgetItem, QMessageBox
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


paths = [
    r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
    r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
]


# Function to list installed applications from the registry
def list_installed_apps():
    installed_apps = []
    for path in paths:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    subkey_name = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, subkey_name) as subkey:
                        try:
                            name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                            # Attempt to get the InstallLocation
                            try:
                                install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                            except FileNotFoundError:
                                install_location = None
                            uninstall_string = winreg.QueryValueEx(subkey, "UninstallString")[0]

                            # Append the app details including the install location
                            installed_apps.append((name, version, uninstall_string, install_location))
                        except FileNotFoundError:
                            continue
        except FileNotFoundError:
            continue
    return installed_apps


# Function to find the main executable
def find_executable(install_location):
    if install_location:
        # Look for an executable in the install location
        for root, dirs, files in os.walk(install_location):
            for file in files:
                if file.lower().endswith('.exe'):
                    return os.path.join(root, file)
    # If no install location, return None
    return None


# Function to open an application
def open_application(executable_path):
    try:
        subprocess.Popen(executable_path, shell=True)
    except Exception as e:
        print(f"Failed to open application: {e}")


class BigWindow(QDialog):
    def __init__(self):
        super().__init__()

        # Set a large size for the window
        self.setWindowTitle("Big Window")
        self.resize(600, 400)

        # A simple label inside the big window
        label = QLabel("This is a big window!", self)
        label.setAlignment(Qt.AlignCenter)

        # Create buttons for the three actions
        open_desktop_button = QPushButton("Open Desktop Folder", self)
        open_desktop_button.clicked.connect(self.open_desktop_folder)

        open_downloads_button = QPushButton("Open Downloads Folder", self)
        open_downloads_button.clicked.connect(self.open_downloads_folder)

        installed_apps_button = QPushButton("Open Installed Apps", self)
        installed_apps_button.clicked.connect(self.show_installed_apps)

        # Set layout and add widgets
        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(open_desktop_button)
        layout.addWidget(open_downloads_button)
        layout.addWidget(installed_apps_button)

        self.installed_apps_dialog = None  # Placeholder for the dialog displaying the apps list

    def open_desktop_folder(self):
        desktop_folder = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        if desktop_folder:
            os.startfile(desktop_folder)  # For Windows
        else:
            print("Desktop folder not found.")

    def open_downloads_folder(self):
        downloads_folder = QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)
        if downloads_folder:
            os.startfile(downloads_folder)  # For Windows
        else:
            print("Downloads folder not found.")

    def show_installed_apps(self):
        if self.installed_apps_dialog is None:
            self.installed_apps_dialog = InstalledAppsDialog(self)
        self.installed_apps_dialog.exec()


class InstalledAppsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Installed Applications")
        self.resize(600, 400)

        # Create search bar and list view
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search for an application...")
        self.search_bar.textChanged.connect(self.filter_apps)

        # Create a list view to display installed applications
        self.app_list_view = QListView(self)
        self.app_list_view.setSelectionMode(QListView.SingleSelection)

        # Create a layout for buttons and list view
        layout = QVBoxLayout(self)
        layout.addWidget(self.search_bar)
        layout.addWidget(self.app_list_view)

        # Create a button to open the selected application folder
        self.open_button = QPushButton("Open Application", self)
        self.open_button.setEnabled(False)  # Disabled initially
        self.open_button.clicked.connect(self.open_selected_application)
        layout.addWidget(self.open_button)

        # Get the list of installed applications and display them
        self.apps_list = self.get_installed_apps()
        self.apps_model = InstalledAppsListModel(self.apps_list)
        self.app_list_view.setModel(self.apps_model)

        # Connect item selection signal
        self.app_list_view.selectionModel().selectionChanged.connect(self.on_selection_changed)

    def get_installed_apps(self):
        # Fetch the list of installed applications using the Windows registry
        return list_installed_apps()

    def filter_apps(self):
        # Filter the applications list based on the search bar input
        filter_text = self.search_bar.text().lower()
        filtered_apps = [app for app in self.apps_list if filter_text in app[0].lower()]
        self.apps_model.update_apps(filtered_apps)

    def on_selection_changed(self):
        # Enable the Open Application button when an application is selected
        selected_indexes = self.app_list_view.selectionModel().selectedIndexes()
        if selected_indexes:
            self.open_button.setEnabled(True)
        else:
            self.open_button.setEnabled(False)

    def open_selected_application(self):
        selected_indexes = self.app_list_view.selectionModel().selectedIndexes()
        if selected_indexes:
            app_name = self.apps_model.data(selected_indexes[0], Qt.DisplayRole)
            selected_app = next(app for app in self.apps_list if app[0] == app_name)

            install_location = selected_app[3]
            executable_path = find_executable(install_location)

            if executable_path:
                open_application(executable_path)
            else:
                print(f"Could not find the main executable for {app_name}.")


class InstalledAppsListModel(QAbstractListModel):
    def __init__(self, apps):
        super().__init__()
        self.apps = apps

    def rowCount(self, parent=QModelIndex()):
        return len(self.apps)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        app_name = self.apps[index.row()]

        if role == Qt.DisplayRole:
            return app_name[0]  # Return the software name (DisplayName)

    def update_apps(self, apps):
        self.beginResetModel()
        self.apps = apps
        self.endResetModel()
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create and show the draggable widget
    window = DraggableWidget()
    window.show()

    sys.exit(app.exec())
