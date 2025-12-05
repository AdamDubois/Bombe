#!/usr/bin/env python
#coding: utf-8
"""
Fichier : RFIDNoBlock.py
Description: Code de test pour le lecteur RFID MFRC522 avec effets lumineux via une bande de LEDs WS2812.
    - Lit les cartes RFID et affiche l'ID et le texte.
    - Permet d'écrire de nouvelles données sur la carte RFID en appuyant sur un bouton poussoir.
    - Utilise une méthode de lecture non bloquante pour éviter de geler le programme.
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
import time

# Initialisation
reader = SimpleMFRC522()
LED = class_DEL.DEL()

# Variables globales
last_couleur = None
id = None
text = None

# Boucle principale
print("Appuyez Ctrl-C pour quitter.")
try:
    while True:
        print("Approchez une carte RFID pour lire...")
        # Lecture non bloquante
        while id is None:
            id, text = reader.read_no_block()  # Utilisation de la méthode non bloquante
            if id is None:
                time.sleep(0.1)  # Petite pause avant de re-essayer
        text = text.strip()
        print(f"Carte lue : ID={id}, Texte={text}")

        if LED.checkCouleur(text) and text != last_couleur:
            last_couleur = text
            LED.set_all_del_color(LED.dict_couleurs[text])
            LED.strip.show()

            # ÉCRIRE SUR LA CARTE
            new_text = input('Nouvelle donnée à écrire : ')
            print("Approchez la carte pour écrire...")
            reader.write(new_text)
            print(f"Écriture terminée : {new_text}")
            time.sleep(0.5)  # Petite pause avant la prochaine lecture

        # Réinitialiser les variables pour la prochaine lecture
        id = None
        text = None

except Exception as e:
    print(f"\nException capturée : {type(e).__name__}: {e}")

except KeyboardInterrupt:
    print("\nArrêt du programme demandé.")

finally:
    print("\nArrêt du programme.")
    LED.eteindre()
    LED.strip.show()
    time.sleep(0.5)
    GPIO.cleanup()
    print("Nettoyage terminé.")