# File: Config.py
# Description: Configuration file for GPIO pin definitions for hardware components and other settings.
# Author: Adam Dubois
# Date: 28 Novembre 2025

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