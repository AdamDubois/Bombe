#!/usr/bin/env python
#coding: utf-8
"""
Fichier : rst_ESP.py
Description: Class pour gérer le reset des ESPs via une pin GPIO.
"""
__author__ = "Adam Dubois et Jérémy Breault"
__version__ = "1.0.1"
__date__ = "2026-04-15"
__maintainer__ = "Adam Dubois"
__email__ = "adamdubois19@hotmail.com"
__status__ = "Production"

import RPi.GPIO as GPIO
import time

# Pin de reset pour les ESPs
reset_pin_RFID = 36
reset_pin_IO = 32
reset_pin_NEO = 22

class ResetESP:
    def __init__(self):
        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(reset_pin_IO, GPIO.OUT)
            GPIO.setup(reset_pin_RFID, GPIO.OUT)
            GPIO.setup(reset_pin_NEO, GPIO.OUT)
            print("Pin de reset configurée pour les ESPs.")
        except Exception as e:
            print(f"Erreur lors de la configuration de la pin de reset: {e}")
    
    def reset_esps(self):
        try:
            print("Pin de reset mise à LOW pour réinitialiser les ESPs.")
            GPIO.output(reset_pin_IO, GPIO.LOW)
            GPIO.output(reset_pin_RFID, GPIO.LOW)
            GPIO.output(reset_pin_NEO, GPIO.LOW)
            time.sleep(0.5)  # Maintenir le reset pendant 0.5 seconde
            GPIO.output(reset_pin_IO, GPIO.HIGH)
            GPIO.output(reset_pin_RFID, GPIO.HIGH)
            GPIO.output(reset_pin_NEO, GPIO.HIGH)
            print("ESP réinitialisés.")
        except Exception as e:
            print(f"Erreur lors du reset des ESPs: {e}")

    def reset_un_esp(self, esp):
        try:
            if esp == "RFID":
                GPIO.output(reset_pin_RFID, GPIO.LOW)
                time.sleep(0.5)
                GPIO.output(reset_pin_RFID, GPIO.HIGH)
                print("ESP RFID réinitialisé.")
            elif esp == "IO":
                GPIO.output(reset_pin_IO, GPIO.LOW)
                time.sleep(0.5)
                GPIO.output(reset_pin_IO, GPIO.HIGH)
                print("ESP IO réinitialisé.")
            elif esp == "NEO":
                GPIO.output(reset_pin_NEO, GPIO.LOW)
                time.sleep(0.5)
                GPIO.output(reset_pin_NEO, GPIO.HIGH)
                print("ESP NEO réinitialisé.")
            else:
                print(f"ESP inconnu: {esp}")
        except Exception as e:
            print(f"Erreur lors du reset de l'ESP {esp}: {e}")
    
    def cleanup(self):
        try:
            print("Nettoyage des GPIO.")
            GPIO.cleanup()
        except Exception as e:
            print(f"Erreur lors du nettoyage des GPIO: {e}")