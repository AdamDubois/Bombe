#!/usr/bin/env python
#coding: utf-8
"""
Fichier : Class_UDP.py
Description: Class pour la gestion de la communication UDP.
    - Permet d'écouter les messages UDP dans un thread séparé pour ne pas bloquer le programme principal
        et permettre une réception asynchrone des messages.
    - Permet de traiter les messages reçus.
    - Quand un objet de cette classe est instancié, le thread est automatiquement démarré.
    - Pour vérifier le dernier message reçu, il suffit de lire la variable publique `last_command`.
    - Pour vérifier l'adresse du dernier expéditeur, il suffit de lire la variable publique `last_addr`.
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
    """Classe pour gérer la communication UDP dans un thread séparé."""
    def __init__(self, port=Config.UDP_LISTEN_PORT, address=Config.UDP_ADDRESS):
        """Initialisation du listener UDP et démarrage du thread."""
        super().__init__(daemon=True)
        self.port = port
        self.address = address
        self.running = True
        self.last_command = None
        self.start()  # Démarre automatiquement le thread
        
    def run(self):
        """Boucle principale du thread pour écouter les messages UDP."""
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
        """Traite les messages reçus via UDP."""
        logger.debug(f"[UDP] Message reçu: {data} de {addr}")
        self.last_command = data
        self.last_addr = addr
        
    def stop(self):
        """Arrêt du thread de réception UDP."""
        self.running = False