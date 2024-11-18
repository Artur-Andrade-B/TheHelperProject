import sys
import os
import winreg
import subprocess
import pygame
import numpy as np
import pyaudio
from PySide6.QtCore import Qt, QPoint, QStandardPaths, QAbstractListModel, QModelIndex, QTimer
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMenu, QDialog, QLineEdit, \
    QListView, QProgressBar
from print_window import PrintWindow

# Importing VoiceRecognizer and speak for voice recognition and TTS
from voice_recognition1 import VoiceRecognizer
from text_to_speech import speak


class DraggableWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window to stay on top
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)

        # Make the widget frameless
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # Create a label to show some text
        self.label = QLabel("Say one of these commands:\n- 'Menu'\n- 'Window'\n- 'Print'\n- 'Quit'", self)

        # Create a button to trigger the radial menu
        self.open_menu_button = QPushButton("Open Radial Menu", self)
        self.open_menu_button.clicked.connect(self.open_radial_menu)

        # Create a button to trigger speech recognition
        self.speech_button = QPushButton("Activate Speech Recognition", self)
        self.speech_button.clicked.connect(self.activate_speech_recognition)

        # Create a progress bar to show audio volume level
        self.audio_level_bar = QProgressBar(self)
        self.audio_level_bar.setRange(0, 100)
        self.audio_level_bar.setValue(0)
        self.audio_level_bar.setTextVisible(False)

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.open_menu_button)
        layout.addWidget(self.speech_button)
        layout.addWidget(self.audio_level_bar)

        # Set the widget's initial size
        self.resize(200, 150)

        # Variables for dragging
        self.dragging = False
        self.drag_position = QPoint()

        # Initialize the voice recognizer (without automatic listening)
        self.voice_recognizer = VoiceRecognizer(language='pt-BR')

        # Initialize pygame mixer for audio (instead of pyaudio)
        pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=1024)

        # Initialize PyAudio for microphone audio monitoring
        self.paudio = pyaudio.PyAudio()
        self.stream = self.paudio.open(format=pyaudio.paInt16,
                                       channels=1,
                                       rate=44100,
                                       input=True,
                                       frames_per_buffer=1024)

        # Timer for updating the audio level
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_audio_level)
        self.timer.start(50)  # Update audio level every 100ms

    def update_audio_level(self):
        """Monitor microphone audio level and update progress bar."""
        # Read data from microphone
        audio_data = self.stream.read(1024)
        # Calculate volume by checking the peak value
        volume = max(abs(int(i)) for i in audio_data)

        # Map volume to progress bar (0-100 scale)
        volume_level = min(int(volume / 5000 * 100), 100)  # Set threshold to 5000 (adjust if needed)
        self.audio_level_bar.setValue(volume_level)

        # Optional: Provide feedback if the volume exceeds a certain threshold
        if volume > 5000:  # Threshold
            speak("Microphone input detected!", language='pt')

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

        # Add a "Open Print Window" action to the menu
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
    def open_documents_folder(self):
        documents_folder = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
        if documents_folder:
            os.startfile(documents_folder)
        else:
            print("Documents folder not found.")

    def open_desktop_folder(self):
        desktop_folder = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        if desktop_folder:
            os.startfile(desktop_folder)
        else:
            print("Desktop folder not found.")

    def open_downloads_folder(self):
        downloads_folder = QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)
        if downloads_folder:
            os.startfile(downloads_folder)
        else:
            print("Downloads folder not found.")

    def show_installed_apps(self):
        if self.installed_apps_dialog is None:
            self.installed_apps_dialog = InstalledAppsDialog(self)
        self.installed_apps_dialog.exec()

    def activate_speech_recognition(self):
        # Start by asking for a command
        speak("Aguardando comando de voz.", language='pt')  # Feedback in Portuguese before listening

        # Listen for the command
        command = self.voice_recognizer.listen()

        if command:
            # Feedback based on the recognized command
            if 'menu' in command:
                speak("Menu radial aberto.", language='pt')
                self.open_radial_menu()

            elif 'window' in command:
                speak("Janela grande aberta.", language='pt')
                self.open_big_window()

            elif 'print' in command:
                speak("Janela de impressão aberta.", language='pt')
                self.open_print_window()

            elif 'documentos'in command:
                speak("Abrindo pasta de documentos.", language='pt')
                self.open_documents_folder()

            elif "downloads"  in command:
                speak("abrindo pasta de downloads", language="pt")
                self.open_documents_folder()

            elif 'quit' or "sair" or "fechar" in command:
                speak("Fechando o aplicativo.", language='pt')
                self.close()
            else:
                speak(f"Desculpe, eu não entendi o comando: {command}",language='pt')
        else:
            speak("Desculpe, não entendi.", language='pt')  # Play audio if no command was heard


# Existing code for listing installed apps, opening applications, etc.
# Function to list installed applications from the registry
def list_installed_apps():
    installed_apps = []
    paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]
    for path in paths:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    subkey_name = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, subkey_name) as subkey:
                        try:
                            name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
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
    return None  # If no install location, return None


# Function to open an application
def open_application(executable_path):
    try:
        subprocess.Popen(executable_path, shell=True)
    except Exception as e:
        print(f"Failed to open application: {e}")


class BigWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Big Window")
        self.resize(600, 400)

        label = QLabel("This is a big window!", self)
        label.setAlignment(Qt.AlignCenter)

        open_desktop_button = QPushButton("Open Desktop Folder", self)
        open_desktop_button.clicked.connect(self.open_desktop_folder)

        open_downloads_button = QPushButton("Open Downloads Folder", self)
        open_downloads_button.clicked.connect(self.open_downloads_folder)

        open_documents_button = QPushButton("Open Documents Folder", self)
        open_documents_button.clicked.connect(self.open_documents_folder)

        installed_apps_button = QPushButton("Open Installed Apps", self)
        installed_apps_button.clicked.connect(self.show_installed_apps)

        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(open_desktop_button)
        layout.addWidget(open_downloads_button)
        layout.addWidget(open_documents_button)
        layout.addWidget(installed_apps_button)

        self.installed_apps_dialog = None

    def open_documents_folder(self):
        documents_folder = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
        if documents_folder:
            os.startfile(documents_folder)
        else:
            print("Documents folder not found.")

    def open_desktop_folder(self):
        desktop_folder = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        if desktop_folder:
            os.startfile(desktop_folder)
        else:
            print("Desktop folder not found.")

    def open_downloads_folder(self):
        downloads_folder = QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)
        if downloads_folder:
            os.startfile(downloads_folder)
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

        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search for an application...")
        self.search_bar.textChanged.connect(self.filter_apps)

        self.app_list_view = QListView(self)
        self.app_list_view.setSelectionMode(QListView.SingleSelection)

        layout = QVBoxLayout(self)
        layout.addWidget(self.search_bar)
        layout.addWidget(self.app_list_view)

        self.open_button = QPushButton("Open Application", self)
        self.open_button.setEnabled(False)
        self.open_button.clicked.connect(self.open_selected_application)
        layout.addWidget(self.open_button)

        self.apps_list = self.get_installed_apps()
        self.apps_model = InstalledAppsListModel(self.apps_list)
        self.app_list_view.setModel(self.apps_model)

        self.app_list_view.selectionModel().selectionChanged.connect(self.on_selection_changed)

    def get_installed_apps(self):
        return list_installed_apps()

    def filter_apps(self):
        filter_text = self.search_bar.text().lower()
        filtered_apps = [app for app in self.apps_list if filter_text in app[0].lower()]
        self.apps_model.update_apps(filtered_apps)

    def on_selection_changed(self):
        selected_indexes = self.app_list_view.selectionModel().selectedIndexes()
        self.open_button.setEnabled(bool(selected_indexes))

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
            return app_name[0]

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
