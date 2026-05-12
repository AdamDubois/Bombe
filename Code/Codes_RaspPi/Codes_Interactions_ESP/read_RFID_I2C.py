#!/usr/bin/env python
#coding: utf-8
"""
Fichier : read_RFID_I2C.py
Description: Ce script permet de lire les données RFID via I2C entre un Raspberry Pi et un ESP32.
"""
__author__ = "Adam Dubois"
__version__ = "1.0.1"
__date__ = "2026-05-12"
__maintainer__ = "Adam Dubois"
__email__ = "adamdubois19@hotmail.com"
__status__ = "Production"

from smbus2 import SMBus, i2c_msg      # Pour l'I2C (sudo pip install smbus2)
import rst_ESP as rst
import time

esp_handler = rst.ResetESP()

# Adresse I2C de l'ESP32 (doit correspondre à SLAVE_ADDR dans ton Arduino)
ESP32_ADDR = 0x11  # (0x0a en hex, 10 en décimal)
I2C_BUS = 1        # Bus I2C habituels sur Pi (bus 1 sur la plupart des modèles)

bus = SMBus(I2C_BUS)

print("Envoi de requêtes I2C vers ESP32, Ctrl+C pour quitter.")
try:
    esp_handler.reset_un_esp("RFID")  # Réinitialiser l'ESP RFID avant de commencer les lectures
    time.sleep(2)  # Attendre un moment pour que l'ESP redémarre
    while True:
        try:
            strReceived = ""
            # Lecture de la réponse
            response = i2c_msg.read(ESP32_ADDR, 256)  # Lire jusqu'à 256 octets
            bus.i2c_rdwr(response)

            for value in response:
                if (value == 0x00):
                    break
                strReceived += chr(value)
            # Convertir la liste d'octets en chaîne
            print("Réponse reçue:", strReceived)
        except Exception as e:
            print("Erreur de lecture I2C:", e)

        #time.sleep(1)

except KeyboardInterrupt:
    print("\nFin du programme !")
finally:
    bus.close()
    esp_handler.cleanup()