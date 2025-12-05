#!/usr/bin/env python
#coding: utf-8
"""
Fichier : TestBoutonRFID.py
Description: Code de test pour un bouton poussoir connecté au Raspberry Pi avec un lecteur RFID MFRC522.
    - Configure un GPIO en entrée avec une résistance de pull-up.
    - Affiche un message lorsque le bouton est appuyé.
    - Utilise un anti-rebond logiciel pour éviter les fausses détections.
    - Gère les interruptions et nettoie correctement les ressources GPIO à la fin.
"""
__author__ = "Adam Dubois et Jérémy Breault"
__version__ = "1.0.1"
__date__ = "2025-12-05"
__maintainer__ = "Adam Dubois"
__email__ = "adamdubois19@hotmail.com"
__status__ = "Production"


import RPi.GPIO as GPIO
import time

from lib.mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

BUTTON_PIN = 16
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Appuyez sur le bouton (Ctrl+C pour quitter)")

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print("Bouton appuyé !")
            time.sleep(0.2)  # Anti-rebond (debounce)
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nArrêt.")
finally:
    GPIO.cleanup()