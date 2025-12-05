#!/usr/bin/env python
#coding: utf-8
"""
Fichier : UART.py
Description: Class pour la gestion de la communication UART.
"""
__author__ = "Adam Dubois et Jérémy Breault"
__version__ = "1.0.1"
__date__ = "2025-12-05"
__maintainer__ = "Adam Dubois"
__email__ = "adamdubois19@hotmail.com"
__status__ = "Production"


import serial
import os

class UART:
    def __init__(self, port='/dev/serial0', baudrate=115200, timeout=1):
        # Vérifier si le port existe et est accessible
        if not os.path.exists(port):
            raise FileNotFoundError(f"Le port {port} n'existe pas")
        
        try:
            self.uart = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=timeout
            )
        except PermissionError as e:
            raise PermissionError(
                f"Erreur de permission: {e}\n"
                f"Solutions possibles:\n"
                f"1. Exécuter avec sudo: sudo python3 {__file__}\n"
                f"2. Ajouter votre utilisateur au groupe dialout: sudo usermod -a -G dialout $USER\n"
                f"3. Modifier les permissions: sudo chmod 666 {port}"
            )
        except serial.SerialException as e:
            raise serial.SerialException(f"Erreur série: {e}")

    def send_message(self, message):
        try:
            message_str = str(message)  # Ajouter un saut de ligne à la fin
            self.uart.write(message_str.encode('utf-8'))
        except Exception as e:
            print(f"Erreur lors de l'envoi du message UART: {e}")

    def close(self):
        self.uart.close()