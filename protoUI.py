#!/usr/bin/env python3
# env: python3 PyQt5
# Auteur: Jeremy Breault
# Date: 2025-10-17
# Description: Code principale pour le fonctionnement de l'interface utilisateur
#              Gère l'integration de la console dite "hacker" dans une fenetre PyQt5.

# =====================================================#
#                        Imports                       #
# =====================================================#
import sys
import random
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFrame, QTextEdit
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont


# =====================================================#
#                    Classe Principale                 #
# =====================================================#

titre_Du_Projet = "Projet InXtremis"#Titre du projet

#=================== Liste de commande de style "hacker" ===================#
COMMANDS = [
    "init_link -addr 10.0.0.19 --sync",
    "auth: token=0x4f2a9c... validated",
    "scan_ports --range 1-65535 --fast",
    "decrypt --keyfile /tmp/key.bin",
    "payload_upload --target 192.168.0.42",
    "grep 'ERROR'/code = 3478 /var/log/syslog | tail -n 50",
    "mount -o remount,rw /",
    "ssh root@198.51.100.10 -p 2222",
    "curl -s http://mirror/pack | tar -xzf -",
    "db.query('SELECT * FROM users WHERE active=1')",
    "watchdog: heartbeat OK",
    "compile --optimize -j8 module_core",
    "inject --mem 0x7ffdf000 --size 0x400",
    "ifconfig eth0 down && ifconfig eth0 up",
    "rm -rf /tmp/.cache && sync",
    "openssl s_client -connect example.com:443",
    "echo 1 > /proc/sys/net/ipv4/ip_forward",
    "nmap -sS -Pn -T4 10.0.0.0/24",
]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        dark_style = """
        QMainWindow {
            background-color: #121212;
            color: #FFFFFF;
        }
        """
        self.setStyleSheet(dark_style)
        self.setWindowTitle("InXtremis") #titre de la fenetre
        self.initUI()
        
    def initUI(self):
        label = QLabel(titre_Du_Projet, self)
        label.setFont(QFont("Forte", 30))
        label.setGeometry(50, 50, 500, 100)
        label.setStyleSheet("color: green;")

        # Créer un frame pour la console hacker
        console_frame = QFrame(self)
        console_frame.setGeometry(30, 900, 1200, 600)
        console_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(5,5,5,0.9); 
                border: 2px solid #00ff00;
                border-radius: 8px;
                padding: 8px;
            }
        """)

        # Titre de la console
        label_console = QLabel("=== CONSOLE SYSTÈME ===", self)
        label_console.setGeometry(30, 870, 400, 30)
        label_console.setStyleSheet("""
            color: #00ff00;
            font-weight: bold;
            text-align: center;
        """)

        # Zone de texte pour afficher les commandes qui défilent
        self.console_text = QTextEdit(console_frame)
        self.console_text.setGeometry(10, 10, 1100, 580)
        self.console_text.setReadOnly(True)  # Lecture seule
        
        # Enlever les barres de défilement
        self.console_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.console_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.console_text.setStyleSheet("""
            QTextEdit {
                background-color: rgba(0,0,0,0.9);
                color: #00ff00;
                font-family: 'Courier New', monospace;
                font-size: 20px;
                border: none;
                padding: 5px;
            }
        """)

        # Variables pour le défilement
        self.command_index = 0
        
        # Démarrer le défilement automatique
        self.demarrer_defilement()

    def demarrer_defilement(self):
        """Démarre le défilement des commandes"""
        # Créer et démarrer le timer - pas de message d'initialisation
        self.timer = QTimer()
        self.timer.timeout.connect(self.nouvelle_commande)
        self.timer.start(2000)  # Nouvelle commande toutes les 2 secondes
        
    def nouvelle_commande(self):
        commande = COMMANDS[self.command_index]
        self.command_index += 1
        
        if self.command_index >= len(COMMANDS):
            self.command_index = 0
        
        timestamp = time.strftime("%H:%M:%S")
        self.console_text.append(f"[{timestamp}] root@inxtremis:~$ {commande}")
        
        # Scroll automatique vers le bas
        scrollbar = self.console_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())


def main():
    app = QApplication(sys.argv)
    window = MainWindow() 
    # window.setWindowFlags(Qt.FramelessWindowHint) #fenetre sans bordure
    window.showFullScreen() #pleine ecran
   
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
    
