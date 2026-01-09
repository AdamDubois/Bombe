#!/usr/bin/env python
#coding: utf-8
"""
Fichier : Class_RFID.py
Description: Class pour la gestion du lecteur RFID.
    - La lecture des tags RFID est effectuée dans un thread séparé pour ne pas bloquer le programme principal 
        lors de l'attente de la lecture et permettre une lecture même lorsque le programme principal est occupé.
    - Permet de mettre en pause et reprendre la lecture RFID sans arrêter le thread.
    - Permet d'écrire des données sur un tag RFID.
    - Permet de nettoyer les données lues.
    - Quand un objet de cette classe est instancié, le thread est automatiquement démarré.
    - Pour vérifier les données lues, il suffit de lire les variables publiques `id` et `text`.
"""
__author__ = "Adam Dubois et Jérémy Breault"
__version__ = "1.0.1"
__date__ = "2025-12-05"
__maintainer__ = "Adam Dubois"
__email__ = "adamdubois19@hotmail.com"
__status__ = "Production"


from lib.mfrc522 import SimpleMFRC522
import threading

class RFIDReader(threading.Thread):
    """Classe pour gérer le lecteur RFID dans un thread séparé."""
    def __init__(self):
        """Initialisation du lecteur RFID et démarrage du thread."""
        super().__init__(daemon=True) # Thread en mode daemon pour s'arrêter avec le programme principal
        self.reader = SimpleMFRC522() # Initialisation du lecteur RFID
        self.id = None
        self.text = None
        self.running = True
        self.paused = False  # Flag pour mettre en pause la lecture
        self.start()  # Démarre automatiquement le thread

    def run(self):
        """Boucle principale du thread pour lire les tags RFID."""
        while self.running:
            # Ne lis que si le lecteur n'est pas en pause
            if not self.paused:
                id, text = self.reader.read_no_block() # Lecture non bloquante
                if id is not None:
                    self.id = id
                    self.text = text.strip()
            
            threading.Event().wait(0.1) # Petite pause pour ne pas surcharger le CPU
        
    def clear_data(self):
        """Nettoie les données lues."""
        self.id = None
        self.text = None

    def write_data(self, text):
        """Écrit des données sur un tag RFID."""
        self.reader.write(text)

    def pause(self):
        """Met en pause la lecture RFID (le thread continue de tourner)"""
        self.paused = True

    def resume(self):
        """Reprend la lecture RFID"""
        self.paused = False

    def stop(self):
        """Arrête complètement le thread"""
        self.running = False
