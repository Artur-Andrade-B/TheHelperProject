from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QProgressBar
from PySide6.QtCore import Qt, QPoint
from main.audio.text_to_speech import speak
from main.audio.voice_recognition import VoiceRecognizer
from main.ui.big_window import BigWindow
from main.ui.print_window import PrintWindow
from main.ui.radial_menu import RadialMenu  # Import RadialMenu class
from main.utils.open_folder import open_documents_folder, open_desktop_folder, open_downloads_folder
from main.utils.registry import list_installed_apps

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

        # Initialize the radial menu
        self.radial_menu = RadialMenu(self)

    def mousePressEvent(self, event):
        """Enable dragging the widget"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        """Handle dragging of the widget"""
        if self.dragging:
            delta = event.globalPosition().toPoint() - self.drag_position
            self.move(self.pos() + delta)
            self.drag_position = event.globalPosition().toPoint()
            event.accept()

    def mouseReleaseEvent(self, event):
        """Stop dragging the widget"""
        self.dragging = False

    def open_radial_menu(self):
        """Method to open the radial menu"""
        self.radial_menu.add_item("Print", self.open_print_window)
        self.radial_menu.add_item("Window", self.open_big_window)
        self.radial_menu.add_item("Quit", self.close)
        self.radial_menu.exec_()  # Open the radial menu

    def open_print_window(self):
        """Opens the Print Window"""
        self.print_window = PrintWindow()
        self.print_window.show()

    def open_big_window(self):
        """Opens the Big Window"""
        self.big_window = BigWindow()
        self.big_window.show()

    def activate_speech_recognition(self):
        # Start by asking for a command
        speak("Aguardando comando de voz.", language='pt')  # Feedback in Portuguese before listening

        # Listen for the command
        command = self.voice_recognizer.listen()

        if command:
            if 'menu' in command:
                speak("Menu radial aberto.", language='pt')
                self.open_radial_menu()

            elif 'window' in command:
                speak("Janela grande aberta.", language='pt')
                self.open_big_window()

            elif 'print' in command:
                speak("Janela de impressão aberta.", language='pt')
                self.open_print_window()

            elif 'documentos' in command:
                speak("Abrindo pasta de documentos.", language='pt')
                open_documents_folder()

            elif "downloads" in command:
                speak("Abrindo pasta de downloads.", language='pt')
                open_downloads_folder()

            elif 'quit' or "sair" or "fechar" in command:
                speak("Fechando o aplicativo.", language='pt')
                self.close()
            else:
                speak(f"Desculpe, eu não entendi o comando: {command}", language='pt')
        else:
            speak("Desculpe, não entendi.", language='pt')  # Play audio if no command was heard
