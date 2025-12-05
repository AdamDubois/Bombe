#!/usr/bin/env python
#coding: utf-8
"""
Fichier : Config.py
Description: Fichier de configuration pour les paramètres matériels et GPIO.
    - Définit les broches GPIO utilisées pour les composants matériels.
    - Spécifie les paramètres de configuration pour la bande de LEDs WS2812.
"""
__author__ = "Adam Dubois et Jérémy Breault"
__version__ = "1.0.1"
__date__ = "2025-12-05"
__maintainer__ = "Adam Dubois"
__email__ = "adamdubois19@hotmail.com"
__status__ = "Production"


import board

#---------------------------------------------------------------------------------------------------------------------------------------#
#                                                                                                                                       #
# Hardware component pin definitions                                                                                                    #
#                                                                                                                                       #
#---------------------------------------------------------------------------------------------------------------------------------------#

# LED Strip
#Pin definition for the LED strip data line
LED_STRIP_PIN = board.A5          # Pin GPIO utilisé pour contrôler les LEDs (doit être PWM)

#Configuration for the LED strip
LED_STRIP_COUNT = 75        # Nombre de LEDs dans la bande (ajustez selon votre bande)

#--------------------------------------------------------------------------#

# UART Configuration
TX_PIN = board.TX  # Pin TX pour UART
RX_PIN = board.RX  # Pin RX pour UART
UART_BAUDRATE = 115200  # Vitesse de communication UART