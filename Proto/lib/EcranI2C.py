from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import ImageFont, ImageDraw, Image
import time

class EcranI2C:
    def __init__(self, adresse=0x3C, largeur=128, hauteur=64):
        self.largeur = largeur
        self.hauteur = hauteur
        self.serial = i2c(port=1, address=adresse)
        self.device = ssd1306(self.serial, width=largeur, height=hauteur, mode="1")
        self.font = ImageFont.load_default()
        self.device.cleanup = False  # Empêche le nettoyage automatique à la fin du script

        # Image en mémoire pour garder ce qui est affiché
        self.image_actuelle = Image.new("1", (self.largeur, self.hauteur), 0)
        self.y_courant = 0 # Position Y pour le prochain texte à ajouter

    def afficher_texte(self, texte, position=(0, 0), duree=1):
        with canvas(self.device) as draw:
            draw.text(position, texte, fill=255, font=self.font)

        # Réinitialise l'image en mémoire
        self.image_actuelle = Image.new("1", (self.largeur, self.hauteur), 0)
        self.y_courant
        time.sleep(duree)

    def ajouter_texte(self, texte, position=None, duree=1):
        if position is None:
            position = (0, self.y_courant)

        # Dessine sur l'image en mémoire
        draw = ImageDraw.Draw(self.image_actuelle)
        draw.text(position, texte, fill=255, font=self.font)
        
        # Envoie l'image à l'écran
        self.device.display(self.image_actuelle)
        
        # Met à jour la position Y pour le prochain texte
        lignes = texte.count('\n') + 1
        self.y_courant += lignes * 16  # ~8 pixels par ligne
        
        time.sleep(duree)

    def effacer_ecran(self):
        """Efface complètement l'écran"""
        self.image_actuelle = Image.new("1", (self.largeur, self.hauteur), 0)
        self.device.display(self.image_actuelle)
        self.y_courant = 0