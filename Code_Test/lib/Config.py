# File: Config.py
# Description: Configuration file for GPIO pin definitions for hardware components and other settings.
# Author: Adam Dubois
# Date: 11 Novembre 2025

# The GPIO pin definitions for the hardware components
# So, for example, GPIO 1 is the pin 28 on the Raspberry Pi header
# Here is the mapping of GPIO --> Pin numbers:
# 3V3 Power  (Pin 1)     | 5V Power  (Pin 2)
# GPIO 1     (Pin 28)    | 5V Power  (Pin 4)
# GPIO 2     (Pin 3)     | Ground   (Pin 6)
# GPIO 3     (Pin 5)     | GPIO 14  (Pin 8)
# GPIO 4     (Pin 7)     | GPIO 15  (Pin 10)
# Ground     (Pin 9)     | GPIO 18  (Pin 12)
# GPIO 17    (Pin 11)    | Ground   (Pin 14)
# GPIO 27    (Pin 13)    | GPIO 23  (Pin 16)
# 3V3 Power  (Pin 17)    | GPIO 24  (Pin 18)
# GPIO 10    (Pin 19)    | Ground   (Pin 20)
# GPIO 9     (Pin 21)    | GPIO 25  (Pin 22)
# GPIO 11    (Pin 23)    | GPIO 8   (Pin 24)
# Ground     (Pin 25)    | GPIO 7   (Pin 26)
# GPIO 0     (Pin 27)    | GPIO 1   (Pin 28)
# GPIO 5     (Pin 29)    | Ground   (Pin 30)
# GPIO 6     (Pin 31)    | GPIO 12  (Pin 32)
# GPIO 13    (Pin 33)    | Ground   (Pin 34)
# GPIO 19    (Pin 35)    | GPIO 16  (Pin 36)
# GPIO 26    (Pin 37)    | GPIO 20  (Pin 38)
# Ground     (Pin 39)    | GPIO 21  (Pin 40)

GPIO1 = 28
GPIO2 = 3
GPIO3 = 5
GPIO4 = 7
GPIO5 = 29
GPIO6 = 31
GPIO7 = 26
GPIO8 = 24
GPIO9 = 21
GPIO10 = 19
GPIO11 = 23
GPIO12 = 32
GPIO13 = 33
GPIO14 = 8
GPIO15 = 10
GPIO16 = 36
GPIO17 = 11
GPIO18 = 12
GPIO19 = 35
GPIO20 = 38
GPIO21 = 40
GPIO22 = 18
GPIO23 = 16
GPIO24 = 18
GPIO25 = 22
GPIO26 = 37
GPIO27 = 13

#---------------------------------------------------------------------------------------------------------------------------------------#
#                                                                                                                                       #
# Hardware component pin definitions                                                                                                    #
#                                                                                                                                       #
#---------------------------------------------------------------------------------------------------------------------------------------#

# SPI
#Pin definitions for SPI communication
SPI_SCK_PIN = 23            # Pin GPIO utilisé pour l'horloge SPI
SPI_MOSI_PIN = 19           # Pin GPIO utilisé pour la ligne de données MOSI SPI
SPI_MISO_PIN = 21           # Pin GPIO utilisé pour la ligne de données MISO SPI

#--------------------------------------------------------------------------#

# RFID Reader
#Pin definitions for the RFID reader
RFID_RESET_PIN = 22         # Pin GPIO utilisé pour réinitialiser le lecteur RFID
RFID_SS_PIN = 24            # Pin GPIO utilisé pour la sélection de puce (Slave Select) du lecteur RFID

#--------------------------------------------------------------------------#

# LED Strip
#Pin definition for the LED strip data line
LED_STRIP_PIN = 18          # Pin GPIO utilisé pour contrôler les LEDs (doit être PWM)

#Configuration for the LED strip
LED_STRIP_COUNT = 75        # Nombre de LEDs dans la bande (ajustez selon votre bande)
LED_STRIP_FREQ_HZ = 800000  # Fréquence du signal LED en hertz (800khz)
LED_STRIP_DMA = 10          # Canal DMA à utiliser pour générer le signal (essayez 10)
LED_STRIP_BRIGHTNESS = 255  # Luminosité des LEDs (0-255)
LED_STRIP_INVERT = False    # True pour inverser le signal (quand on utilise un transistor NPN)
LED_STRIP_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53