import RPi.GPIO as GPIO
from lib.mfrc522 import SimpleMFRC522
import class_DEL
import threading
import time

# Initialisation
reader = SimpleMFRC522()
LED = class_DEL.DEL()

# Variables globales
last_id = None
last_text = None
last_couleur = None
thread_Stop = False

# Thread
def rfid_reader_thread():
    global last_id, last_text, thread_Stop

    print("[RFID] Thread RFID démarré.")
    while not thread_Stop:
        # Attendre une carte (bloquant)
        id, text = reader.read()
        text = text.strip()
        print(f"[RFID] Carte lue : ID={id}, Texte={text}")

        last_id = id
        last_text = text

        time.sleep(0.5)  # Petite pause pour éviter une boucle trop rapide