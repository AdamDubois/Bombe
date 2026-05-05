"""
Nom du fichier : jsonreceive.py
Description : Module de réception et de traitement des données JSON pour l’interface graphique.

Ce module :
- Met en place un serveur TCP (socket) en écoute
- Reçoit des données JSON provenant du système de jeu
- Met à jour les états internes (game_start, enigme, RFID)
- Expose ces états à l’interface via des propriétés Qt (PySide6)
- Gère un minuteur interne avec décrémentation automatique

Fonctionnalités principales :
- Communication réseau via socket (TCP)
- Synchronisation thread-safe (threading + verrou)
- Signalisation des changements vers l’interface (Qt Signals)
- Gestion d’un timer de jeu

Paramètres réseau :
- Adresse : 0.0.0.0
- Port : 5000

Dépendances :
- PySide6 (QtCore)
- socket, threading, json, time

Auteur : Jérémy Breault
Date : 2026-04-25
"""

# liste des imports
import socket      # communication réseau
import threading   # pour l'utilisation des threads
import json        # données JSON
import time        # gestion du temps
 
# intégration avec QT 
from PySide6.QtCore import QObject, Property, Signal, Slot


# Configuration réseau
HOST = "0.0.0.0"
PORT = 5000


class JsonReceive(QObject):
    """
    Classe responsable de :
    - Recevoir des données JSON via un serveur TCP
    - Mettre à jour les états du jeu
    - Exposer ces états à l’interface Qt via des propriétés et signaux
    - Gérer un timer interne
    """

    # Signaux Qt émis lors de changements de valeurs
    gameStartChanged = Signal()
    enigmeChanged = Signal()
    rfidChanged = Signal()
    timeRemainingChanged = Signal()


    def __init__(self):
        super().__init__()

        # États internes du jeu
        self._game_start = False
        self._enigme = 0
        self._rfid = [False, False, False, False]
        self._time_remaining = 300 # 5 minutes 

        # Variables de contrôle des threads
        self._running = False
        self._timer_running = True

        # sécuriter
        self._lock = threading.Lock()

        # Lancement du thread du timer en arrière-plan
        timer_thread = threading.Thread(target=self._run_timer, daemon=True)
        timer_thread.start()



    # =========================
    # Propriétés exposées à Qt
    # =========================
    @Property(bool, notify=gameStartChanged)
    def game_start(self):
        # retourne l'état du jeu
        return self._game_start

    @Property(int, notify=enigmeChanged)
    def enigme(self):
        # retourne le numéro de l'énigme en cours
        return self._enigme

    @Property("QVariantList", notify=rfidChanged)
    def rfid(self):
        # retourne l'état des quatre module RFID
        return self._rfid

    @Property(int, notify=timeRemainingChanged)
    def time_remaining(self):
        # retourne le temps restant
        return self._time_remaining


    # =========================
    # Slots Qt (appelables depuis QML)
    # =========================
    @Slot()
    def reset_timer(self):
        # reset du timer
        with self._lock:
            self._time_remaining = 300 # 5 minutes
        self.timeRemainingChanged.emit()

    @Slot(int)
    def set_timer(self, value):
        # pour définir une valeur pour le timer
        with self._lock:
            self._time_remaining = max(0, int(value))
        self.timeRemainingChanged.emit()


    def partir_serveur(self):
        # Démarre le serveur TCP dans un thread
        if self._running:
            return
        self._running = True
        thread = threading.Thread(target=self._run_server, daemon=True)
        thread.start()

    def arrêter_serveur(self):
        # Arrête le serveur et le timer
        self._running = False
        self._timer_running = False

    def _run_timer(self):
        # timer pour le jeu
        while self._timer_running:
            time.sleep(1)

            emit_needed = False


            with self._lock:
                if self._game_start and self._time_remaining > 0:
                    self._time_remaining -= 1
                    emit_needed = True
                    current_time = self._time_remaining

            if emit_needed:
                self.timeRemainingChanged.emit()



    # =========================
    # Boucle serveur
    # =========================

    def _run_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((HOST, PORT))
            server.listen(5)

            print(f"Serveur JSON en écoute sur {HOST}:{PORT}")

            while self._running:
                try:
                    # Attente d’une connexion client
                    conn, addr = server.accept()
                except OSError:
                    break

                # Réception des données
                with conn:
                    raw = conn.recv(4096)
                    if not raw:
                        continue
                    
                    # Décodage UTF-8
                    message_str = raw.decode("utf-8").strip()
                    if not message_str:
                        continue

                    for line in message_str.split("\n"):
                        line = line.strip()
                        if not line:
                            continue

                        # conversion JSON vers un dictionnaire Python
                        try:
                            data = json.loads(line)
                        except json.JSONDecodeError:
                            print("JSON invalide :", line)
                            continue
                        
                        # mise à jour des valeurs
                        self._update_values(data)



    # =========================
    # Mise à jour des données
    # =========================

    def _update_values(self, data):

        # Mise à jour du status du jeu
        if "game_start" in data:
            new_game_start = bool(data["game_start"])
            if self._game_start != new_game_start:
                self._game_start = new_game_start
                self.gameStartChanged.emit()
                print(f"[GAME_START] {self._game_start}")

        # Mise à jour de l'énigme en cours 
        if "enigme" in data:
            enigme = int(data["enigme"])
            if self._enigme != enigme:
                self._enigme = enigme
                self.enigmeChanged.emit()
                print(f"[ENIGME] {self._enigme}")

        # Mise à jours des modules RFID
        if "rfid" in data:
            rfid = list(data["rfid"])
            if len(rfid) == 4:
                rfid = [bool(x) for x in rfid]
                if self._rfid != rfid:
                    self._rfid = rfid
                    self.rfidChanged.emit()
                    print(f"[RFID] {self._rfid}")