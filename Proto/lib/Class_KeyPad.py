#!/usr/bin/env python
#coding: utf-8
"""
Fichier : Class_KeyPad.py
Description: Class pour la gestion du pavé numérique via GPIO.
    - La lecture des touches est effectuée dans un thread séparé pour ne pas bloquer le programme principal 
        et permettre une détection asynchrone des appuis sur les touches.
    - Quand un objet de cette classe est instancié, le thread est automatiquement démarré.
    - Pour vérifier l'état des touches, il suffit de lire la variable publique `key_pressed`.
"""
__author__ = "Adam Dubois et Jérémy Breault"
__version__ = "1.0.1"
__date__ = "2026-01-09"
__maintainer__ = "Adam Dubois"
__email__ = "adamdubois19@hotmail.com"
__status__ = "Production"

import RPi.GPIO as GPIO
import lib.Config as Config
import threading

class KeyPad(threading.Thread):
    """Classe pour gérer le pavé numérique via GPIO dans un thread séparé."""
    def __init__(self):
        """Initialisation des broches GPIO pour le pavé numérique et démarrage du thread de lecture."""
        super().__init__(daemon=True) # Thread en mode daemon pour s'arrêter avec le programme principal

        self.key_pressed = None # Variable publique pour indiquer la touche pressée

        GPIO.setmode(GPIO.BOARD) # Utilisation de la numérotation physique des broches

        for row_pin in Config.KEYPAD_ROW_PINS:
            GPIO.setup(row_pin, GPIO.OUT)
            GPIO.output(row_pin, GPIO.HIGH)

        for col_pin in Config.KEYPAD_COL_PINS:
            GPIO.setup(col_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.running = True
        self.start()

    def run(self):
        """Boucle principale du thread pour lire l'état du pavé numérique."""
        while self.running:
            for row_index, row_pin in enumerate(Config.KEYPAD_ROW_PINS):
                GPIO.output(row_pin, GPIO.LOW)
                for col_index, col_pin in enumerate(Config.KEYPAD_COL_PINS):
                    if GPIO.input(col_pin) == GPIO.LOW:
                        self.key_pressed = Config.KEYPAD_BUTTONS[row_index][col_index]
                        # Attendre que la touche soit relâchée
                        while GPIO.input(col_pin) == GPIO.LOW:
                            threading.Event().wait(0.1)
                GPIO.output(row_pin, GPIO.HIGH)

            threading.Event().wait(0.1)  # Petite pause pour éviter une boucle trop rapide

    def stop(self):
        """Arrêt du thread de lecture du pavé numérique."""
        self.running = False
        GPIO.cleanup()