import pygame
import pyaudio
from PySide6.QtCore import QTimer
from main.audio.text_to_speech import speak

class AudioMonitor:
    def __init__(self):
        # Initialize pygame mixer for audio
        pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=1024)

        # Initialize PyAudio for microphone audio monitoring
        self.paudio = pyaudio.PyAudio()
        self.stream = self.paudio.open(format=pyaudio.paInt16,
                                       channels=1,
                                       rate=44100,
                                       input=True,
                                       frames_per_buffer=1024)

        # Timer for updating the audio level
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_audio_level)
        self.timer.start(50)  # Update audio level every 50ms

    def update_audio_level(self):
        """Monitor microphone audio level and update progress bar."""
        # Read data from microphone
        audio_data = self.stream.read(1024)
        # Calculate volume by checking the peak value
        volume = max(abs(int(i)) for i in audio_data)

        # Map volume to progress bar (0-100 scale)
        volume_level = min(int(volume / 5000 * 100), 100)  # Set threshold to 5000 (adjust if needed)

        # Optional: Provide feedback if the volume exceeds a certain threshold
        if volume > 5000:  # Threshold
            speak("Microphone input detected!", language='pt')
