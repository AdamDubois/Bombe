#!/usr/bin/env python
#coding: utf-8
"""
Fichier : UART.py
Description: Code pour gérer la communication UART de manière asynchrone sur ESP32-S3 Feather.
    - Utilise busio.UART pour la communication série.
    - Fournit des fonctions pour lire et écrire des données via UART.
    - Gère les données reçues de manière non bloquante avec polling.
    - Supporte la lecture de lignes complètes terminées par un saut de ligne (\n).
"""
__author__ = "Adam Dubois et Jérémy Breault"
__version__ = "1.0.1"
__date__ = "2025-12-05"
__maintainer__ = "Adam Dubois"
__email__ = "adamdubois19@hotmail.com"
__status__ = "Production"


import busio
import lib.Config as Config

# Configuration de l'UART
uart = busio.UART(Config.TX_PIN, Config.RX_PIN, baudrate=Config.UART_BAUDRATE)
uart.timeout = 0  # Non-bloquant

# Buffer pour accumuler les données reçues
receive_buffer = ""

async def write_uart(message="Hello from ESP32!\n"):
    uart.write(message.encode("utf-8"))  # Envoi des données
    print("Données envoyées :", message.strip())

async def read_uart_line():
    """Lit les données UART de manière asynchrone avec polling"""
    global receive_buffer
    
    try:
        # Lecture non-bloquante des données disponibles
        data = uart.read(64)  # Lit jusqu'à 64 bytes
        
        if data is not None:
            # Convertir en string et ajouter au buffer
            try:
                new_data = data.decode("utf-8")
                receive_buffer += new_data
                print(f"Buffer: '{receive_buffer}'")
                
                # Chercher une ligne complète (terminée par \n)
                if "\n" in receive_buffer:
                    lines = receive_buffer.split("\n")
                    complete_line = lines[0].strip()
                    # Garder le reste dans le buffer
                    receive_buffer = "\n".join(lines[1:])
                    
                    if complete_line:  # Si la ligne n'est pas vide
                        print(f"Ligne complète reçue: '{complete_line}'")
                        return complete_line
                        
            except UnicodeError:
                print("Erreur de décodage UTF-8, données ignorées")
                receive_buffer = ""  # Vider le buffer en cas d'erreur
                
    except Exception as e:
        print(f"Erreur UART: {e}")
    
    return None

async def read_uart_polling():
    """Version alternative qui retourne immédiatement les données disponibles"""
    try:
        data = uart.read(32)  # Lit jusqu'à 32 bytes
        if data is not None:
            decoded = data.decode("utf-8").strip()
            if decoded:  # Si il y a des données non-vides
                print(f"Données UART reçues: '{decoded}'")
                return decoded
    except UnicodeError:
        print("Erreur de décodage UTF-8, données ignorées")
    except Exception as e:
        print(f"Erreur UART: {e}")
    
    return None

def uart_available():
    """Vérifie si des données sont disponibles dans l'UART"""
    return uart.in_waiting > 0