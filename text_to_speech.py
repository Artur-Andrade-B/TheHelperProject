from gtts import gTTS
import os
import pygame
import time
import tempfile

def speak(text, language='pt'):
    try:
        # Generate TTS audio using gTTS
        tts = gTTS(text=text, lang=language)

        # Create a temporary file to store the TTS audio
        fd, temp_file_path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)  # Close the file descriptor so it can be used

        # Save the generated TTS audio to the temporary file
        tts.save(temp_file_path)

        # Initialize pygame mixer to play the audio
        pygame.mixer.init()

        # Load and play the audio file
        pygame.mixer.music.load(temp_file_path)
        pygame.mixer.music.play()

        # Wait until the audio is done playing before proceeding
        while pygame.mixer.music.get_busy():  # Check if the music is still playing
            time.sleep(0.1)  # Sleep for a small amount to avoid high CPU usage

        # Optionally, remove the temporary file after playing
        os.remove(temp_file_path)

    except Exception as e:
        print(f"Error in text-to-speech: {e}")
