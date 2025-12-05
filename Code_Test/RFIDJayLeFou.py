#!/usr/bin/env python
#coding: utf-8
"""
Fichier : RFIDJayLeFou.py
Description: Code de test pour le lecteur RFID MFRC522 avec effets lumineux via une bande de LEDs WS2812.
    - Lit les cartes RFID et affiche l'ID et le texte.
    - Permet d'écrire de nouvelles données sur la carte RFID en appuyant sur un bouton poussoir.
    - Change les effets lumineux de la bande de LEDs en fonction du texte lu sur la carte RFID.
    - Utilise un thread pour gérer les effets lumineux de manière fluide.
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

BUTTON_PIN = 16
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Variables globales
last_couleur = None
id = None
text = None

# Thread pour l'effet de lumière
def light_effect_thread():
    global last_couleur
    couleur = None
    try:
        while True:
            if last_couleur is not None:
                if couleur != last_couleur:
                    couleur = last_couleur
                for i in range(10):
                    LED.heartbeat(LED.dict_couleurs[couleur], wait_ms=50)
                    if couleur != last_couleur:
                        couleur = last_couleur
                for i in range(2):
                    LED.flash(LED.dict_couleurs[couleur], wait_ms=200, brightness=128)
                    if couleur != last_couleur:
                        couleur = last_couleur
            else:
                time.sleep(0.1)

    except Exception as e:
        print(f"[Light Effect] Erreur : {e}")

# Démarrer le thread des effets lumineux
thread = threading.Thread(target=light_effect_thread, daemon=True)
thread.start()

# Boucle principale
print("Appuyez Ctrl-C pour quitter.")
print("Approchez une carte RFID pour lire...")
try:
    while True:
        # Lecture non bloquante
        id, text = reader.read_no_block()  # Utilisation de la méthode non bloquante

        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print("Bouton appuyé !")
            time.sleep(0.2)  # Anti-rebond (debounce)

            # ÉCRIRE SUR LA CARTE
            new_text = input('Nouvelle donnée à écrire : ')
            print("Approchez la carte pour écrire...")
            reader.write(new_text)
            print(f"Écriture terminée : {new_text}")
            time.sleep(0.5)  # Petite pause avant la prochaine lecture

        if id is None:
            time.sleep(0.1)  # Petite pause avant de re-essayer
        elif id is not None:
            text = text.strip()
            print(f"Carte lue : ID={id}, Texte={text}")

            if LED.checkCouleur(text) and text != last_couleur:
                last_couleur = text

            # Réinitialiser les variables pour la prochaine lecture
            id = None
            text = None

        time.sleep(0.1)

except Exception as e:
    print(f"\n[Main] Exception capturée : {type(e).__name__}: {e}")

except KeyboardInterrupt:
    print("\nArrêt du programme demandé.")

finally:
    print("\nArrêt du programme.")
    LED.eteindre()
    LED.strip.show()
    time.sleep(0.5)
    GPIO.cleanup()
    print("Nettoyage terminé.")
