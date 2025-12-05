#!/usr/bin/env python
#coding: utf-8
"""
Fichier : New_RFID_ReadWrite.py
Description: Code de test pour la lecture et l'écriture RFID utilisant la bibliothèque lib.Class_RFID.
    - Initialise le lecteur RFID.
    - Lit l'UID de la carte RFID présente.
    - Écrit des données sur la carte RFID.
    - Lit et affiche les données écrites pour vérification.
    - Utilise des threads pour gérer la lecture RFID de manière non bloquante.
    - Permet d'interrompre le programme proprement avec Ctrl+C.
    - Contrôle les LEDs WS2812 pour indiquer l'état de la lecture/écriture.
    - Implémente un verrou pour la gestion des données partagées entre threads.
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

# Variables partagées
last_id = None
last_text = None
last_couleur = None
data_lock = threading.Lock()
stop_reading = threading.Event()  # Contrôle du thread

# Thread de lecture RFID
def rfid_reader_thread():
    global last_id, last_text
    print("[RFID] Thread RFID démarré.")
    try:
        while not stop_reading.is_set():
            # Attendre une carte (bloquant, mais contrôlé)
            print("[RFID] Approchez une carte RFID pour lire...")
            id, text = reader.read()
            print("[RFID] Carte détectée.")
            if stop_reading.is_set():
                break
            text = text.strip()
            print(f"[RFID] Carte lue : ID={id}, Texte={text}")

            with data_lock:
                last_id = id
                last_text = text

    except Exception as e:
        if not stop_reading.is_set():
            print(f"[RFID] Erreur lecture RFID : {e}")
    finally:
        print("[RFID] Thread RFID arrêté.")

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
                    text = input('[Main] Nouvelle donnée à écrire : ')
                    print("[Main] Approchez la carte pour écrire...")

                    # 1. Arrêter la lecture
                    stop_reading.set()
                    time.sleep(1)  # Laisser le temps au thread de sortir

                    try:
                        # 2. Écrire
                        reader.write(text)
                        print("[Main] Écriture réussie !")
                        time.sleep(2)  # Pause pour éviter les lectures immédiates
                    except Exception as e:
                        print(f"[Main] Échec écriture : {e}")
                    finally:
                        # 3. Relancer la lecture
                        stop_reading.clear()
                        # Relancer le thread
                        thread = threading.Thread(target=rfid_reader_thread, daemon=True)
                        #thread.start()

                # Réinitialiser
                last_id = None
                last_text = None

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nArrêt du programme.")
    LED.eteindre()
    LED.strip.show()

finally:
    time.sleep(0.5)
    GPIO.cleanup()
    print("Nettoyage terminé.")