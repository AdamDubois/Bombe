#!/usr/bin/env python
#coding: utf-8
"""
Fichier : Bouton.py
Description: Class pour la gestion du bouton via GPIO.
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

class Bouton(threading.Thread):
    bouton_Gauche_appuye = False
    bouton_Droite_appuye = False

    def __init__(self):
        super().__init__(daemon=True)
        self.bouton_Gauche_pin = Config.BUTTON_G_PIN
        GPIO.setup(self.bouton_Gauche_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.bouton_Droite_pin = Config.BUTTON_D_PIN
        GPIO.setup(self.bouton_Droite_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.running = True

    def run(self):
        while self.running:
            if GPIO.input(self.bouton_Gauche_pin) == GPIO.LOW:
                self.bouton_Gauche_appuye = True

            if GPIO.input(self.bouton_Droite_pin) == GPIO.LOW:
                self.bouton_Droite_appuye = True

    def stop(self):
        self.running = False