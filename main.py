import sys
import speech_recognition as sr
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
import pyttsx3
import threading

class SpeechEncryptionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Speech Encryption App")

        # Create UI components
        self.label = QLabel("Press the 'Record' button and start speaking...")
        self.button_record = QPushButton("Record")
        self.button_record.clicked.connect(self.record_button_clicked)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button_record)

        # Set the layout to the central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Speech Recognition and Text-to-Speech objects
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

        # Generate private key (keep it secure!)
        self.private_key = Fernet.generate_key()

    def record_button_clicked(self):
        # Disable the record button during processing
        self.button_record.setEnabled(False)
        self.label.setText("Recording...")

        # Start a separate thread for recording and processing
        threading.Thread(target=self.process_speech).start()

    def process_speech(self):
        # Speech-to-Text Conversion
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)

        text = self.recognizer.recognize_google(audio)

        # Encryption
        cipher_suite = Fernet(self.private_key)
        encrypted_message = cipher_suite.encrypt(text.encode())

        # Decryption
        decrypted_message = cipher_suite.decrypt(encrypted_message).decode()

        # Text-to-Speech Conversion
        self.speak_message(decrypted_message)

        # Update the UI on the main thread
        self.update_ui(text, decrypted_message)

    def speak_message(self, message):
        self.engine.say(message)
        self.engine.runAndWait()

    def update_ui(self, original_text, decrypted_text):
        self.label.setText(f"Original Text: {original_text}\nDecrypted Text: {decrypted_text}")
        self.button_record.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpeechEncryptionApp()
    window.show()
    sys.exit(app.exec_())
