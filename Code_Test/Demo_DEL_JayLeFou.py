#!/usr/bin/env python
#coding: utf-8
"""
Fichier : Demo_DEL_JayLeFou.py
Description: Code de test pour l'animation personnalisée "JayLeFou" des LEDs WS2812.
    - Utilise la bibliothèque lib.class_DEL pour contrôler les LEDs.
    - Implémente une animation personnalisée nommée "JayLeFou".
    - Permet d'interrompre le programme proprement avec Ctrl+C.
"""
__author__ = "Adam Dubois et Jérémy Breault"
__version__ = "1.0.1"
__date__ = "2025-12-05"
__maintainer__ = "Adam Dubois"
__email__ = "adamdubois19@hotmail.com"
__status__ = "Production"


import lib.class_DEL as class_DEL
from lib.rpi_ws281x import Color

LED = class_DEL.DEL()

def main():
    """Programme principal pour tester les animations LED."""
    try:
        print('Contrôle de bande LED WS2812 - Appuyez Ctrl-C pour quitter.')
        while True:
            LED.JayLeFou("rouge")  # Effet personnalisé Jaylefou en rouge
    except KeyboardInterrupt:
        print("\nProgramme interrompu par l'utilisateur")
        LED.eteindre()
        LED.strip.show()
        print("LEDs éteintes - Nettoyage terminé")

if __name__ == '__main__':
    main()