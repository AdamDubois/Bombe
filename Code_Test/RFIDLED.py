import RPi.GPIO as GPIO
from lib.mfrc522 import SimpleMFRC522
import code.Code_Test.lib.class_DEL as class_DEL
import threading
import time

# Initialisation
reader = SimpleMFRC522()
LED = class_DEL.DEL()

# Variable pour stocker les dernières données lues
last_couleur = None
last_id = None
last_text = None
data_lock = threading.Lock()  # Pour éviter les conflits d'accès

# Fonction exécutée dans le thread
def rfid_reader_thread():
    global last_id, last_text
    print("Thread RFID démarré. En attente de carte...")
    try:
        while True:
            id, text = reader.read()
            text = text.strip()
            print(f"[RFID] Carte détectée ! ID: {id}, Texte: {text}")

            with data_lock:
                last_id = id
                last_text = text

    except Exception as e:
        print(f"Erreur dans le thread RFID : {e}")
    finally:
        print("Thread RFID terminé.")

# Démarrer le thread
thread = threading.Thread(target=rfid_reader_thread, daemon=True)
thread.start()

# Boucle principale (non bloquante)
try:
    while True:
        # Ici, tu peux faire autre chose en parallèle
        # Par exemple, vérifier si une nouvelle carte a été lue
        with data_lock:
            if last_text is not None and last_text != last_couleur:
                print(f"[Main] Mise à jour LEDs avec : {last_text}")
                couleur = LED.checkCouleur(last_text)
                if couleur != -1:
                    last_couleur = last_text
                    LED.set_all_del_color(couleur)
                    LED.strip.show()
                # Réinitialiser pour éviter de répéter
                last_id = None
                last_text = None

        time.sleep(0.1)  # Petit sleep pour ne pas surcharger le CPU

except KeyboardInterrupt:
    print("\nProgramme interrompu par l'utilisateur")
    LED.eteindre()
    LED.strip.show()
    print("LEDs éteintes.")

finally:
    GPIO.cleanup()
    print("Nettoyage GPIO terminé.")