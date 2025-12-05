#!/usr/bin/env python
#coding: utf-8
"""
Fichier : Bouton.py
Description: Class pour la gestion du bouton via GPIO.
    - La lecture des boutons est effectuée dans un thread séparé pour ne pas bloquer le programme principal 
        et permettre une détection asynchrone des appuis sur les boutons.
    - Quand un objet de cette classe est instancié, le thread est automatiquement démarré.
    - Pour vérifier l'état des boutons, il suffit de lire les variables publiques `bouton_Gauche_appuye` et `bouton_Droite_appuye`.
"""
__author__ = "Adam Dubois et Jérémy Breault"
__version__ = "1.0.1"
__date__ = "2025-12-05"
__maintainer__ = "Adam Dubois"
__email__ = "adamdubois19@hotmail.com"
__status__ = "Production"


import RPi.GPIO as GPIO
import lib.Config as Config
import threading
import time

class Bouton(threading.Thread):
    bouton_Gauche_appuye = False # Indicateur d'appui sur le bouton gauche
    bouton_Droite_appuye = False # Indicateur d'appui sur le bouton droit

    """Initialisation des broches GPIO pour les boutons et démarrage du thread de lecture."""
    def __init__(self):
        super().__init__(daemon=True)
        GPIO.setmode(GPIO.BOARD) # Utilisation de la numérotation physique des broches
        self.bouton_Gauche_pin = Config.BUTTON_G_PIN
        GPIO.setup(self.bouton_Gauche_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Configuration en entrée avec résistance de pull-up

        self.bouton_Droite_pin = Config.BUTTON_D_PIN
        GPIO.setup(self.bouton_Droite_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Configuration en entrée avec résistance de pull-up

        self.running = True
        self.start()

    """Boucle principale du thread pour lire l'état des boutons."""
    def run(self):
        while self.running:
            time.sleep(0.1)  # Petite pause pour éviter une boucle trop rapide
            if GPIO.input(self.bouton_Gauche_pin) == GPIO.LOW:
                self.bouton_Gauche_appuye = True

            if GPIO.input(self.bouton_Droite_pin) == GPIO.LOW:
                self.bouton_Droite_appuye = True

    """Arrêt du thread de lecture des boutons."""
    def stop(self):
        self.running = False