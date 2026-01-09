# Projet Bombe - InXtremis

## Description

Un projet Raspberry Pi utilisant RFID, LEDs WS2812, écran OLED et différentes communication pour créer un système de désamorçage de bombe interactif. Pour l'instant, il n'y a pas de système de désamorçage, il n'y a que les différents codes pour tester les composantes qui sont utilisées.

## Fonctionnalités

### Fonctionnalités principales
- **Lecture/Écriture RFID** : Authentification et stockage de séquences (threaded, non bloquant)
- **Effets DEL programmables** : Animations visuelles (heartbeat, flash, arc-en-ciel) contrôlées par ESP32-S3 Feather
- **Affichage OLED** : Interface utilisateur temps réel avec écran I2C
- **Communication Réseau** : Serveur UDP pour contrôle distant
- **Communication Série** : Interface UART avec ESP32-S3 Feather
- **Gestion de boutons** : Interface utilisateur physique avec Threads
- **Interface graphique** : Console style "hacker" avec PyQt5
- **Système de Logging** : Traçabilité complète des événements

## Architecture du Projet

```
Bombe-main/
├── Code_Test/          # Scripts de test et développement
│   ├── pi-rfid/           # Utilitaires RFID basiques
│   ├── lib/               # Bibliothèques de test
│   │   ├── class_DEL.py       # Classe LED WS2812
│   │   ├── Config.py          # Configuration test
│   │   └── mfrc522/           # Module RFID
│   ├── Demo_DEL_JayLeFou.py   # Test animations LED
│   ├── I2C_Ecran.py           # Test écran OLED
│   ├── RFIDReadWrite.py       # Test RFID lecture/écriture
│   ├── RFIDNoBlock.py         # Test RFID non-bloquant
│   ├── TestBouton.py          # Test boutons
│   ├── UART.py                # Test communication série
│   ├── UDP.py                 # Test communication UDP
│   ├── protoUI.py             # Interface graphique PyQt5
│   └── test_threads.py        # Test multithreading
├── Proto/             # Version prototype principale
│   ├── lib/           # Modules principaux
│   │   ├── Config.py          # Configuration GPIO/Hardware
│   │   ├── Class_RFID.py      # Gestion RFID threaded
│   │   ├── Class_EcranI2C.py  # Contrôle écran OLED
│   │   ├── Class_UDP.py       # Communication réseau
│   │   ├── Class_UART.py      # Communication série
│   │   ├── Class_Bouton.py    # Gestion boutons threaded
│   │   ├── Log.py             # Système de logging
│   │   └── mfrc522/           # Module RFID
│   └── Proto.py       # Script principal
├── ESP32/             # Code pour ESP32-S3 Feather
│   ├── lib/               # Bibliothèques ESP32
│   │   ├── Config.py         # Configuration GPIO ESP32
│   │   ├── class_DEL.py      # Contrôle LEDs WS2812
│   │   └── UART.py           # Communication série ESP32
│   └── code.py            # Code principal CircuitPython
├── img/               # Images pour l'interface utilisateur
└── README.md          # Documentation
```

## Prérequis

### Matériel requis
- Raspberry Pi
- Module RFID MFRC522
- Bande DEL WS2812 (75 LEDs)
- Écran OLED I2C SSD1306 (128x64)
- Bouton-poussoir (2x)
- Cartes RFID
- ESP32-S3 Feather

### Logiciels requis
- python3
- python3-pip
- python3-dev
- python3-venv
- python3-spidev
- python3-smbus
- python3-pil
- python3-serial
- git
- i2c-tools
- libfreetype6-dev
- libjpeg-dev
- build-essential
- luma.core
- luma.oled
- fonts-dejavu

## Installation

### 1. Cloner le Projet
```bash
git clone https://github.com/AdamDubois/Bombe.git
cd Bombe-main
```

### 2. Configuration GPIO
Vérifiez les connexions selon `lib/Config.py`

### 3. Logiciels requis
```bash
#-----------------------------------------------#
# Système                                       #
#-----------------------------------------------#
Sudo apt update
Sudo apt upgrade
sudo apt install python3 python3-pip python3-dev python3-venv git
sudo raspi-config #(Activer SPI, I2C et UART dans Interface Options)

#-----------------------------------------------#
# Dépendances Python principales                #
#-----------------------------------------------#

# Bibliothèque pour la communication SPI
sudo apt install python3-spidev

# Bibliothèque pour la communication avec l'écran OLED
sudo apt install -y python3-pip python3-dev python3-smbus i2c-tools libfreetype6-dev libjpeg-dev build-essential #(pour les dépendances)
sudo apt install python3-pil #(pour la gestion de l'affichage, utiliser par Luma.oled)
/bin/pip3 install luma.core --break-system-packages #(pour installer Luma)
/bin/pip3 install luma.oled --break-system-packages #(pour installer Luma)
sudo apt-get install fonts-dejavu #(Pour la font avec les accents)

# Bibliothèque pour la communication UART
sudo apt install python3-serial
```

## Utilisation

### Mode Prototype (toutes les fonctionnalités en un seul script)
```bash
cd Proto
sudo python3 Proto.py
```

### Scripts de Test (Fonctionnalités individuelles)
```bash
cd Code_Test

# Test RFID non-bloquant
sudo python3 RFIDNoBlock.py

# Test RFID lecture/écriture avec threading
sudo python3 RFIDReadWrite.py

# Test LEDs avec animations
sudo python3 Demo_DEL_JayLeFou.py

# Test Écran OLED I2C
python3 I2C_Ecran.py

# Test Boutons GPIO
sudo python3 TestBouton.py

# Test Communication UART
python3 UART.py

# Test Communication UDP
python3 UDP.py

# Interface Graphique PyQt5
python3 protoUI.py

# Test Threading
python3 test_threads.py
```

## Configuration

### Configuration GPIO (`lib/Config.py`)
```python
# LEDs WS2812 (si utilisé par le Raspberry Pi)
LED_STRIP_PIN = 18          # GPIO PWM
LED_STRIP_COUNT = 75        # Nombre de LEDs
LED_STRIP_BRIGHTNESS = 255  # Luminosité (0-255)

# RFID MFRC522
RFID_RESET_PIN = 22         # GPIO Reset
RFID_SS_PIN = 24           # SPI Slave Select

# Écran OLED I2C
# Adresse 0x3C par défaut (128x64)

# Boutons
BUTTON_G_PIN = 15          # Bouton gauche
BUTTON_D_PIN = 13          # Bouton droite

# Communication
UDP_LISTEN_PORT = 12345    # Port UDP
UDP_ADDRESS = "0.0.0.0"    # Interface d'écoute

# UART
UART_PORT = "/dev/serial0"  # Port série
UART_BAUDRATE = 115200      # Vitesse de communication
```

### Mode Debug
```python
# Dans lib/Config.py
DEBUG_MODE = True  # Active les logs détaillés
```

## Composants matériels

### Schéma de Connexion GPIO

| Composant | GPIO/Pin | Fonction |
|-----------|----------|----------|
| **RFID MFRC522** |
| SDA/SS | GPIO 24 | Slave select |
| SCK | GPIO 23 | SPI Clock |
| MOSI | GPIO 19 | Master out |
| MISO | GPIO 21 | Master in |
| RST | GPIO 22 | Reset |
| **LEDs WS2812 (si utilisé par le Raspberry Pi)** |
| Data | GPIO 18 | Signal PWM |
| **Écran I2C** |
| SDA | GPIO 3 | I2C Data |
| SCL | GPIO 5 | I2C Clock |
| **ESP32-S3 Feather (UART)** |
| TX | GPIO 14 | UART Transmit |
| RX | GPIO 15 | UART Receive |
| **Boutons** |
| Bouton G | GPIO 15 | Pull-up interne |
| Bouton D | GPIO 13 | Pull-up interne |

## Débogage

### Problèmes courants

**RFID ne fonctionne pas**
```bash
# Vérifier SPI activé
sudo raspi-config
# Interface Options → SPI → Activer

# Test connexions
sudo python3 -c "import spidev; print('SPI OK')"
```

**Les DEL ne s'allument pas**
(si le Raspberry Pi les utilise)
```bash
# Vérifier permissions
sudo usermod -a -G gpio $USER
sudo reboot

# Test PWM
sudo python3 -c "import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM); print('GPIO OK')"
```

**Écran I2C non détecté**
```bash
# Scanner bus I2C
sudo i2cdetect -y 1

# Activer I2C
sudo raspi-config
# Interface Options → I2C → Activer
```

### Logs de Debug
```python
# Activer logs détaillés
DEBUG_MODE = True  # dans Config.py

# Consulter logs
tail -f /var/log/syslog | grep python
```

## Auteurs
- **Adam Dubois** - Configuration GPIO et hardware
- **Jeremy Breault** - Interface PyQt5 et UI

## Collaborateurs
- **ChatGPT** - Assistance à la rédaction de la documentation et du code
- **Grok** - Assistance à la rédaction de la documentation et du code
- **Copilot** - Assistance à la rédaction de la documentation et du code
- **Warp** - Assistance à la rédaction de la documentation et du code