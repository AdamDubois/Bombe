#!/usr/bin/env python
#coding: utf-8
"""
Fichier : RFIDLED.py
Description: Code de test pour le lecteur RFID MFRC522 avec effets lumineux via une bande de LEDs WS2812.
    - Lit les cartes RFID et affiche l'ID et le texte.
    - Change les effets lumineux de la bande de LEDs en fonction du texte lu sur la carte RFID.
    - Utilise un thread pour lire les cartes RFID de manière non bloquante.
    - Gère les interruptions et nettoie correctement les ressources GPIO à la fin.
"""
__author__ = "Adam Dubois et Jérémy Breault"
__version__ = "1.0.1"
__date__ = "2025-12-05"
__maintainer__ = "Adam Dubois"
__email__ = "adamdubois19@hotmail.com"
__status__ = "Production"


import RPi.GPIO as GPIO
from lib.mfrc522 import SimpleMFRC522
import lib.class_DEL as class_DEL
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