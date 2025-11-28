import RPi.GPIO as GPIO
from lib.mfrc522 import SimpleMFRC522
import threading

class RFIDReader(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.reader = SimpleMFRC522()
        self.id = None
        self.text = None
        self.lock = threading.Lock()
        self.running = True
        self.paused = False  # Flag pour mettre en pause la lecture

    def run(self):
        while self.running:
            # Ne lis que si le lecteur n'est pas en pause
            if not self.paused:
                id, text = self.reader.read_no_block()
                if id is not None:
                    with self.lock:
                        self.id = id
                        self.text = text.strip()
            # Petite pause pour ne pas surcharger le CPU
            threading.Event().wait(0.1)

    def get_data(self):
        with self.lock:
            return self.id, self.text
        
    def clear_data(self):
        with self.lock:
            self.id = None
            self.text = None

    def write_data(self, text):
        self.reader.write(text)

    def pause(self):
        """Met en pause la lecture RFID (le thread continue de tourner)"""
        self.paused = True

    def resume(self):
        """Reprend la lecture RFID"""
        self.paused = False

    def stop(self):
        """Arrête complètement le thread"""
        self.running = False
