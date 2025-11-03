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
stop_reading = threading.Event()  # Contrôle du thread

# Thread
def rfid_reader_thread():
    global last_id, last_text, stop_reading

    print("[RFID] Thread RFID démarré.")
    try:
        while not stop_reading.is_set():
            # Attendre une carte (bloquant)
            id, text = reader.read()
            text = text.strip()
            print(f"[RFID] Carte lue : ID={id}, Texte={text}")

            last_id = id
            last_text = text

            time.sleep(0.5)  # Petite pause pour éviter une boucle trop rapide
    except Exception as e:
        if not stop_reading.is_set():
            print(f"[RFID] Erreur lecture RFID : {e}")
    finally:
        print("[RFID] Thread RFID arrêté.")

# Démarrer le thread
thread = threading.Thread(target=rfid_reader_thread, daemon=True)
thread.start()

# Boucle principale
print("[Main] Appuyez Ctrl-C pour quitter.")
try:
    while True:
        # Lecture
        if last_text is not None and last_text != last_couleur:
            print(f"[Main] Nouvelle couleur détectée : {last_text}")
            couleur = LED.checkCouleur(last_text)
            if couleur != -1:
                last_couleur = last_text
                LED.set_all_del_color(couleur)
                LED.strip.show()

                # Écriture
                try:
                    # Arrêter le thread pour débloquer le RFID
                    stop_reading.set()
                    time.sleep(0.5)  # Attendre que le thread se termine

                    text = input('Nouvelle donnée à écrire : ')
                    print("[Main] Approchez la carte pour écrire...")
                    reader.write(text)
                    print("[Main] Écriture réussie !")
                    time.sleep(1)  # Pause pour éviter les lectures immédiates

                except Exception as e:
                    print(f"[Main] Échec écriture : {e}")

                finally:
                    # Relancer le thread
                    stop_reading.clear()
                    thread = threading.Thread(target=rfid_reader_thread, daemon=True)
                    thread.start()

except KeyboardInterrupt:
    print("\n[Main] Arrêt du programme demandé par l'utilisateur.")

finally:
    # Nettoyage
    thread_Stop = True
    thread.join()
    LED.eteindre()
    LED.strip.show()
    GPIO.cleanup()
    print("[Main] Programme terminé.")