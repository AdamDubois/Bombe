# Projet Bombe - InXtremis

Un projet Raspberry Pi utilisant RFID, LEDs WS2812, écran OLED et communication pour créer un système de désamorçage de bombe interactif.

## Description

Ce projet implémente un système de désamorçage de bombe interactif utilisant un Raspberry Pi. Le système combine plusieurs technologies :
- Lecteur RFID
- Bande de LEDs WS2812 pour les effets visuels contrôlés par un ESP32-S3 Feather
- Écran OLED I2C pour l'affichage d'informations
- Communication UDP pour l'interaction réseau
- Communication UART série pour le contrôle d'un ESP32-S3 Feather
- Interface utilisateur PyQt5 avec console style "hacker"

## Fonctionnalités

### Fonctionnalités Principales
- **Lecture/Écriture RFID** : Authentification et stockage de séquences
- **Effets LED Programmables** : Animations visuelles (heartbeat, flash, arc-en-ciel) contrôlées par ESP32-S3 Feather
- **Affichage OLED** : Interface utilisateur temps réel
- **Communication Réseau** : UDP pour contrôle distant
- **Communication Série** : Interaction avec ESP32-S3 Feather
- **Interface Graphique** : Console style "hacker" avec PyQt5

## Architecture du Projet

```
Bombe-main/
├── Code_Test/          # Scripts de test et développement
|   ├── pi-rfid/       # Utilitaires RFID basiques
│   ├── lib/           # Bibliothèques de test
│   └── *.py           # Scripts de test individuels
├── Proto/             # Version prototype principale
│   ├── lib/           # Modules principaux
│   │   ├── Config.py      # Configuration GPIO/Hardware
│   │   ├── RFID.py        # Gestion RFID threaded
│   │   ├── EcranI2C.py    # Contrôle écran OLED
│   │   ├── UDP.py         # Communication réseau
│   │   ├── UART.py        # Communication série
│   │   └── Log.py         # Système de logging
│   └── Proto.py       # Script principal
├── ESP32/             # Stockage du code ESP32-S3 Feather
│   ├── lib/               # Bibliothèques ESP32
│   │   ├── Config.py         # Configuration des GPIO ESP32
│   │   ├── class_DEL.py      # Contrôle des LEDs WS2812
│   │   └── UART.py           # Communication série ESP32
│   └── code.py            # Code principal ESP32-S3 Feather
├── img/               # Images pour l'interface utilisateur
└── README.md          # Documentation
```

## Prérequis

### Matériel Requis
- Raspberry Pi
- Module RFID MFRC522
- Bande LED WS2812 (75 LEDs)
- Écran OLED I2C SSD1306 (128x64)
- Boutons poussoirs (2x)
- Cartes RFID
- ESP32-S3 Feather

### Logiciels Requis
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

## Installation

### 1. Cloner le Projet
```bash
git clone https://github.com/AdamDubois/Bombe.git
cd Bombe-main
```

### 2. Configuration GPIO
Vérifiez les connexions selon `lib/Config.py` :
- **RFID** : SPI (MOSI=19, MISO=21, SCK=23, SS=24, RST=22)
- **LEDs WS2812** : GPIO 18 (PWM) (si utilisé par le raspberry pi)
- **Écran I2C** : SDA=3, SCL=5 (adresse 0x3C)
- **Boutons** : GPIO 15 (gauche), GPIO 13 (droite)

## Utilisation

### Mode Prototype (Toutes les fonctionnalités en un seul script)
```bash
cd Proto
sudo python3 Proto.py
```

### Scripts de Test (Fonctionnalités individuelles)
```bash
cd Code_Test

# Test RFID
sudo python3 RFIDNoBlock.py

# Test LEDs
sudo python3 Demo_DEL_JayLeFou.py

# Test Écran
python3 I2C_Ecran.py

# Interface Graphique
python3 protoUI.py

# etc.
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
```

### Mode Debug
```python
# Dans lib/Config.py
DEBUG_MODE = True  # Active les logs détaillés
```

## Composants Matériels

### Schéma de Connexion GPIO

| Composant | GPIO/Pin | Fonction |
|-----------|----------|----------|
| **RFID MFRC522** |
| SDA/SS | GPIO 24 | Slave Select |
| SCK | GPIO 23 | SPI Clock |
| MOSI | GPIO 19 | Master Out |
| MISO | GPIO 21 | Master In |
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

### Problèmes Courants

**RFID ne fonctionne pas**
```bash
# Vérifier SPI activé
sudo raspi-config
# Interface Options → SPI → Activer

# Test connexions
sudo python3 -c "import spidev; print('SPI OK')"
```

**LEDs ne s'allument pas**
(Si utilisé par le Raspberry Pi)
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