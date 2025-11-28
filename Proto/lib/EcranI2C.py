from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import ImageFont
import time

class EcranI2C:
    def __init__(self, adresse=0x3C, largeur=128, hauteur=64):
        self.serial = i2c(port=1, address=adresse)
        self.device = ssd1306(self.serial, width=largeur, height=hauteur, mode="1")
        self.font = ImageFont.load_default()
        self.device.cleanup = False  # Empêche le nettoyage automatique à la fin du script

    def afficher_texte(self, texte, position=(0, 0), duree=1):
        with canvas(self.device) as draw:
            draw.text(position, texte, fill=255, font=self.font)
        time.sleep(duree)