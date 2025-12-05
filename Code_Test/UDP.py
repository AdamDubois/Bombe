#!/usr/bin/env python
#coding: utf-8
"""
Fichier : UDP.py
Description: Code pour un serveur UDP simple qui contrôle une bande de LEDs WS2812 connectée au Raspberry Pi.
    - Écoute les messages UDP sur un port spécifié.
    - Allume ou éteint les LEDs en fonction des commandes reçues.
    - Utilise la bibliothèque socket pour la communication réseau.
    - Utilise une classe personnalisée pour gérer les LEDs.
    - Gère les logs pour le débogage et le suivi des événements.
"""
__author__ = "Adam Dubois et Jérémy Breault"
__version__ = "1.0.1"
__date__ = "2025-12-05"
__maintainer__ = "Adam Dubois"
__email__ = "adamdubois19@hotmail.com"
__status__ = "Production"


import socket
import logging
import sys
sys.path.insert(0, '..')
from lib.Config import DEBUG_MODE
import lib.class_DEL as led
logging.basicConfig(
    level=logging.DEBUG if DEBUG_MODE else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

LED = led.DEL()

UDP_IP = "0.0.0.0"
UDP_PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
logger.info(f"UDP Server démarré sur {UDP_IP}:{UDP_PORT}")

while True:
    data, addr = sock.recvfrom(512)
    logger.debug(f"Message reçu: {data} de {addr}")
    
    if data == b'LED=1\n':
        logger.info("Commande: LED allumée (vert)")
        LED.set_all_del_color((0, 255, 0))
        LED.strip.show()
    elif data == b'LED=0\n':
        logger.info("Commande: LED éteinte")
        LED.set_all_del_color((0, 0, 0))
        LED.strip.show()
