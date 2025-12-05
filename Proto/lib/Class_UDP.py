#!/usr/bin/env python
#coding: utf-8
"""
Fichier : UDP.py
Description: Class pour la gestion de la communication UDP.
"""
__author__ = "Adam Dubois et Jérémy Breault"
__version__ = "1.0.1"
__date__ = "2025-12-05"
__maintainer__ = "Adam Dubois"
__email__ = "adamdubois19@hotmail.com"
__status__ = "Production"


import lib.Config as Config
from lib.Log import logger
import socket
import threading

class UDPListener(threading.Thread):
    def __init__(self, port=Config.UDP_LISTEN_PORT, address=Config.UDP_ADDRESS):
        super().__init__(daemon=True)
        self.port = port
        self.address = address
        self.running = True
        self.last_command = None
        
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.address, self.port))
        logger.info(f"[UDP] UDP Listener démarré sur le port {self.port}")
        
        while self.running:
            try:
                data, addr = sock.recvfrom(512)
                self.on_receive(data, addr)
            except Exception as e:
                logger.error(f"[UDP] Erreur UDP: {e}")
            
    def on_receive(self, data, addr):
        logger.debug(f"[UDP] Message reçu: {data} de {addr}")
        self.last_command = data
        
        if data == b'LED=1\n':
            logger.info("[UDP] Commande: LED allumée")
            # Ajouter ici le code GPIO pour allumer la LED
        elif data == b'LED=0\n':
            logger.info("[UDP] Commande: LED éteinte")
            # Ajouter ici le code GPIO pour éteindre la LED
        
    def stop(self):
        self.running = False