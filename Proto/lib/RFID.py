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

    def run(self):
        while self.running:
            id, text = self.reader.read_no_block()
            if id is not None:
                with self.lock:
                    self.id = id
                    self.text = text.strip()

    def get_data(self):
        with self.lock:
            return self.id, self.text
        
    def clear_data(self):
        with self.lock:
            self.id = None
            self.text = None

    def write_data(self, text):
        self.reader.write(text)

    def get_running(self):
        return self.running

    def set_running(self):
        self.running = True

    def stop(self):
        self.running = False