#!/usr/bin/env python
#coding: utf-8
"""
Fichier : I2C_Ecran.py
Description: Code de test pour l'écran OLED I2C utilisant la bibliothèque luma.oled.
    - Initialise l'écran OLED SSD1306 via I2C.
    - Affiche le texte "Fonctionne" pendant 1 seconde normalement, mais puisque device.cleanup est défini sur False,
      l'écran conserve l'affichage même après la fin du script.
"""
__author__ = "Adam Dubois et Jérémy Breault"
__version__ = "1.0.1"
__date__ = "2025-12-05"
__maintainer__ = "Adam Dubois"
__email__ = "adamdubois19@hotmail.com"
__status__ = "Production"


from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import ImageFont
import time

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64, mode="1")

font = ImageFont.load_default()

device.cleanup = False # Empêche le nettoyage automatique à la fin du script


with canvas(device) as draw:
    draw.text((0, 0), "Fonctionne", fill=255, font=font)
time.sleep(1)
