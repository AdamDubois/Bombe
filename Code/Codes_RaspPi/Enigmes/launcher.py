import json
import socket
import threading
import time
import subprocess
import sys

import RPi.GPIO as GPIO

from rst_ESP import ResetESP

from Bouton.EnigmeBouton import Bouton
from RFID.RFID import RFID
from Switchs.Switchs import Switchs

MAIN_UI = "/home/admin/Documents/Projet_InXtremis/code/Code/Codes_RaspPi/Qt/Interface_9avril/OverClockUI/OverClock/main.py"

HOST = "127.0.0.1"
PORT = 5000

BUTTON_PIN = 40  # Pin physique 40 (BOARD)
DEBOUNCE_SECONDS = 0.2
LOOP_SLEEP_SECONDS = 0.05


class launcher:
    def __init__(self):
        # Globale
        self.stop = False

        # Reset des ESPs au lancement du launcher
        self.esp_reset = ResetESP()
        #self.esp_reset.reset_esps()

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

        # Enigmes
        self.enigme = 0
        self.e_rfid = None
        self.e_bouton = None
        self.e_switchs = None

        print("Lancement de l'interface graphique...")
        self.ui_process = subprocess.Popen([sys.executable, MAIN_UI])
        time.sleep(5)  # Attendre que l'interface se lance correctement

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

    def stop_launcher(self):
        print("Arret du launcher...")
        self.stop = True
        GPIO.cleanup()

        self.esp_reset.cleanup()
        self.esp_reset = None

        if self.e_rfid is not None:
            self.e_rfid.close()
            self.e_rfid = None

        if self.e_bouton is not None:
            self.e_bouton.close()
            self.e_bouton = None

        if self.e_switchs is not None:
            self.e_switchs.close()
            self.e_switchs = None

        if self.ui_process is not None:
            try:
                self.ui_process.terminate()
                self.ui_process.wait(timeout=5)
            except Exception:
                self.ui_process.kill()

    def play(self):
        if self.stop:
            self.stop_launcher()

        else:
            if self.bouton_appuye:
                self.bouton_appuye = False
                self.enigme += 1
                print(f"Passage a l'enigme suivante: {self.enigme}")
                self.ui_message["enigme"] = self.enigme
                self.send_state()

            match self.enigme:
                case 0:
                    pass

                case 1:
                    if self.ui_message["game_start"] is False:
                        self.ui_message["game_start"] = True
                        self.send_state()

                    if self.e_rfid is None:
                        self.e_rfid = RFID()
                    self.e_rfid.play()
                    for i in range(4):
                        self.ui_message["rfid"][i] = self.e_rfid.bonnes_cartes[i]
                        print()
                    self.send_state()
                    if self.e_rfid.fini:
                        self.enigme += 1
                        print(f"Enigme RFID terminee. Passage a l'enigme suivante: {self.enigme}")
                        self.ui_message["enigme"] = self.enigme
                        self.send_state()
                case 2:
                    if self.e_bouton is None:
                        self.e_bouton = Bouton()
                    self.e_bouton.play()
                    if self.e_bouton.fini:
                        self.enigme += 1
                        print(f"Enigme bouton terminee. Passage a l'enigme suivante: {self.enigme}")
                        self.ui_message["enigme"] = self.enigme
                        self.send_state()
                case 3:
                    if self.e_switchs is None:
                        self.e_switchs = Switchs()
                    self.e_switchs.play()
                    if self.e_switchs.fini:
                        self.enigme += 1
                        print(f"Enigme Switchs terminee. Passage a l'enigme suivante: {self.enigme}")
                        self.ui_message["enigme"] = self.enigme
                        self.send_state()
                case 4:
                    pass # Écran de victoire géré par l'interface, on attend que le bouton soit pressé pour recommencer
                case 5:
                    print("Toutes les enigmes sont terminées. Recommencement au début.")
                    #self.esp_reset.reset_esps()

                    self.e_rfid.close()
                    self.e_rfid = None
                    self.e_bouton.close()
                    self.e_bouton = None
                    self.e_switchs.close()
                    self.e_switchs = None

                    self.enigme = 0
                    self.ui_message["game_start"] = False
                    self.ui_message["enigme"] = self.enigme
                    self.send_state()

                    time.sleep(2)  # Petite pause pour s'assurer que les ESPs ont le temps de redémarrer avant de relancer les énigmes

if __name__ == "__main__":
    launcher_instance = launcher()
    try:
        while True:
            launcher_instance.play()
            time.sleep(LOOP_SLEEP_SECONDS)
    except KeyboardInterrupt:
        launcher_instance.stop_launcher()