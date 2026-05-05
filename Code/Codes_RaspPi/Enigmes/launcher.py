import json
import socket
import threading
import time

import RPi.GPIO as GPIO

HOST = "127.0.0.1"
PORT = 5000

BUTTON_PIN = 40  # Pin physique 40 (BOARD)
DEBOUNCE_SECONDS = 0.2
LOOP_SLEEP_SECONDS = 0.05


class launcher:
    def __init__(self):
        # Globale
        self.stop = False

        # UI
        self.ui_message = {
            "game_start": False,
            "enigme": 0,
            "rfid": [False, False, False, False],
        }

        # Bouton de skip
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.state = GPIO.input(BUTTON_PIN)
        self.last_state = GPIO.input(BUTTON_PIN)
        self.last_press_time = 0.0
        self.now = time.time()
        self.bouton_appuye = False

        self.start()

    def bouton_thread(self):
        while not self.stop:
            self.state = GPIO.input(BUTTON_PIN)
            self.now = time.time()
            # Appui detecte sur front descendant (pull-up: repos=HIGH, appui=LOW)
            if self.last_state == GPIO.HIGH and self.state == GPIO.LOW:
                if self.now - self.last_press_time >= DEBOUNCE_SECONDS:
                    self.last_press_time = self.now
                    print("Bouton presse -> demande de passage a l'etape suivante")
                    self.bouton_appuye = True
            self.last_state = self.state
            time.sleep(0.01)

    def send_state(self):
        data = json.dumps(self.ui_message) + "\n"
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST, PORT))
            client.sendall(data.encode("utf-8"))
            client.close()
            print(f"Etat UI envoye: {self.ui_message}")
        except Exception as e:
            print(f"Erreur socket UI: {e}")

    def start(self):
        bouton_thread = threading.Thread(target=self.bouton_thread, daemon=True)
        bouton_thread.start()