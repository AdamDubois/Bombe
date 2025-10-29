import RPi.GPIO as GPIO
from lib.mfrc522 import SimpleMFRC522
import class_DEL
import threading
import time

# Initialisation
reader = SimpleMFRC522()
LED = class_DEL.DEL()

# Variables partagées
last_id = None
last_text = None
last_couleur = None
data_lock = threading.Lock()
stop_reading = threading.Event()  # Contrôle du thread

# Thread de lecture RFID
def rfid_reader_thread():
    global last_id, last_text
    print("Thread RFID démarré.")
    try:
        while not stop_reading.is_set():
            # Attendre une carte (bloquant, mais contrôlé)
            id, text = reader.read()
            time.sleep(0.5)  # Petit délai pour éviter les lectures multiples rapides
            if stop_reading.is_set():
                break
            text = text.strip()
            print(f"[RFID] Carte lue : ID={id}, Texte={text}")

            with data_lock:
                last_id = id
                last_text = text

    except Exception as e:
        if not stop_reading.is_set():
            print(f"Erreur lecture RFID : {e}")
    finally:
        print("Thread RFID arrêté.")

# Démarrer le thread
thread = threading.Thread(target=rfid_reader_thread, daemon=True)
thread.start()

# Boucle principale
try:
    while True:
        with data_lock:
            if last_text is not None and last_text != last_couleur:
                print(f"[Main] Nouvelle couleur détectée : {last_text}")
                couleur = LED.checkCouleur(last_text)
                if couleur != -1:
                    last_couleur = last_text
                    LED.set_all_del_color(couleur)
                    LED.strip.show()

                    # ÉCRIRE SUR LA CARTE
                    text = input('Nouvelle donnée à écrire : ')
                    print("Approchez la carte pour écrire...")

                    # 1. Arrêter la lecture
                    stop_reading.set()
                    time.sleep(0.5)  # Laisser le temps au thread de sortir

                    try:
                        # 2. Écrire
                        reader.write(text)
                        print("Écriture réussie !")
                    except Exception as e:
                        print(f"Échec écriture : {e}")
                    finally:
                        # 3. Relancer la lecture
                        stop_reading.clear()
                        # Relancer le thread
                        thread = threading.Thread(target=rfid_reader_thread, daemon=True)
                        thread.start()

                # Réinitialiser
                last_id = None
                last_text = None

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nArrêt du programme.")
    stop_reading.set()
    LED.eteindre()
    LED.strip.show()

finally:
    stop_reading.set()
    time.sleep(0.5)
    GPIO.cleanup()
    print("Nettoyage terminé.")