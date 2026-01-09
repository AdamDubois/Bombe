#!/usr/bin/env python
#coding: utf-8
"""
Fichier : Proto.py
Description: Programme principal pour gérer les interactions entre les composants matériels via GPIO, I2C, SPI, UART et UDP.
"""
__author__ = "Adam Dubois et Jérémy Breault"
__version__ = "1.0.1"
__date__ = "2025-12-05"
__maintainer__ = "Adam Dubois"
__email__ = "adamdubois19@hotmail.com"
__status__ = "Production"


import time
import RPi.GPIO as GPIO
from lib.Class_UDP import UDPListener
from lib.Class_EcranI2C import EcranI2C
from lib.Class_RFID import RFIDReader
from lib.Class_UART import UART
from lib.Class_Bouton import Bouton
from lib.Class_KeyPad import KeyPad
from lib.Log import logger

#-----------------------------------------------#
# Configuration initiale du programme           #
#-----------------------------------------------#
boutons = Bouton()

#-----------------------------------------------#
# Configuration du KeyPad                       #
#-----------------------------------------------#
keypad = KeyPad()

#-----------------------------------------------#
# Initialisation de l'écran I2C                 #
#-----------------------------------------------#
# Créer une instance de l'écran I2C
ecran = EcranI2C()

#-----------------------------------------------#
# Initialisation du RFID                        #
#-----------------------------------------------#
rfid_reader = RFIDReader()

#-----------------------------------------------#
# Initialisation du listener UDP                #
#-----------------------------------------------#
# Démarrer le listener UDP
listener = UDPListener()

#-----------------------------------------------#
# Initialisation du module UART                 #
#-----------------------------------------------#
uart_handler = UART()

#-----------------------------------------------#
# Boucle principale du programme                #
#-----------------------------------------------#
logger.info("[Proto] Programme principal démarré. Le serveur UDP écoute en arrière-plan.")
logger.warning("[Proto] Programme principal démarré. Appuyez sur Ctrl+C pour arrêter.")
ecran.afficher_texte("Programme démarré", position=(0, (ecran.hauteur/2)))
time.sleep(2)
ecran.effacer_ecran()
try:
    while True:
        time.sleep(0.1)  # Petite pause pour éviter une boucle trop rapide

        if listener.last_command:
            logger.warning(f"[Proto] Dernière commande: {listener.last_command}")
            ecran.afficher_texte(f"Cmd: {listener.last_command}", position=(0,0))
            if listener.last_command == b'LED=1\n':
                uart_handler.send_message("SOLID_WHITE")
            elif listener.last_command == b'LED=0\n':
                uart_handler.send_message("OFF")
            listener.last_command = None

        if rfid_reader.id is not None:
            logger.warning(f"[Proto] RFID détecté: ID={rfid_reader.id}, Texte={rfid_reader.text}")
            ecran.afficher_texte(f"RFID ID:{rfid_reader.id}\n{rfid_reader.text}", position=(0, 16))
            uart_handler.send_message(rfid_reader.text)
            rfid_reader.clear_data()

        if boutons.bouton_Gauche_appuye:
            logger.warning("[Proto] Bouton appuyé !")
            rfid_reader.pause()  # Mets en pause la lecture, ne l'arrête pas complètement
            msg = input("[Proto] Entrez le texte à écrire sur le RFID: ")
            logger.debug(f"[Proto] Écriture des données sur le RFID: {msg}")
            rfid_reader.write_data(msg)
            rfid_reader.resume()  # Reprend la lecture
            logger.warning("[Proto] Données écrites sur le RFID.")
            boutons.bouton_Gauche_appuye = False

        if keypad.key_pressed is not None:
            logger.warning(f"[Proto] Touche du KeyPad pressée: {keypad.key_pressed}")
            ecran.afficher_texte(f"KeyPad: {keypad.key_pressed}", position=(0, 32))
            keypad.key_pressed = None



#-----------------------------------------------#
# Arrêt propre du programme                     #
#-----------------------------------------------#
# Gérer l'arrêt propre du programme Ctrl+C
except KeyboardInterrupt:
    logger.warning("[Proto] Arrêt demandé par l'utilisateur (Ctrl+C).")

# Dans tous les cas, s'assurer que tout est arrêté correctement
finally:
    logger.warning("[Proto] Arrêt du programme...")
    listener.stop() # Arrête le listener UDP
    listener.join(timeout=2) # Attend la fin du thread UDP
    uart_handler.close() # Ferme le port UART
    boutons.stop() # Arrête le thread des boutons
    boutons.join(timeout=2) # Attend la fin du thread des boutons
    rfid_reader.stop() # Arrête le thread RFID
    rfid_reader.join(timeout=2) # Attend la fin du thread RFID
    ecran.effacer_ecran() # Efface l'écran avant de quitter
    GPIO.cleanup() # Nettoie les configurations GPIO
    logger.warning("[Proto] Programme terminé.")