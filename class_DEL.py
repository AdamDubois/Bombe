import time
# from more_itertools import strip
from rpi_ws281x import PixelStrip, Color

class DEL:
    """Classe pour gérer une bande de LEDs WS2812."""

    def __init__(self):
        """Initialise la bande de LEDs avec les paramètres par défaut."""
        # Configuration des LEDs WS2812
        self.LED_COUNT = 75          # Nombre de LEDs dans la bande (ajustez selon votre bande)
        self.LED_PIN = 18           # Pin GPIO utilisé pour contrôler les LEDs (doit être PWM)
        self.LED_FREQ_HZ = 800000   # Fréquence du signal LED en hertz (800khz)
        self.LED_DMA = 10           # Canal DMA à utiliser pour générer le signal (essayez 10)
        self.LED_BRIGHTNESS = 255   # Luminosité des LEDs (0-255)
        self.LED_INVERT = False     # True pour inverser le signal (quand on utilise un transistor NPN)
        self.LED_CHANNEL = 0        # set to '1' for GPIOs 13, 19, 41, 45 or 53

        # Créer l'objet PixelStrip
        self.strip = PixelStrip(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)

        # Initialiser la bibliothèque (doit être appelé une fois avant les autres fonctions)
        self.strip.begin()

    
    def set_brightness(self, brightness):
        """Définit la luminosité de la bande de LEDs."""
        self.strip.setBrightness(brightness)
        self.strip.show()

    def set_del_color(self, index, color, brightness=255):
        """Définit la couleur d'une LED spécifique dans la bande."""
        # color = Color(color[0], color[1], color[2]) # Convertir la couleur en format Color
        self.strip.setPixelColor(index, color) # Définir la couleur de la LED
        self.strip.setBrightness(brightness)
        self.strip.show() # Mettre à jour la bande pour afficher la nouvelle couleur

    def set_all_del_color(self, color, brightness=255):
        """Définit la même couleur pour toutes les LEDs dans la bande."""
        # color = Color(color[0], color[1], color[2]) # Convertir la couleur en format Color
        for i in range(self.strip.numPixels()): # Pour chaque LED dans la bande
            self.set_del_color(i, color, brightness) # Définir la couleur de la LED

    def eteindre(self):
        """Éteint toutes les LEDs dans la bande."""
        self.set_all_del_color(Color(0, 0, 0)) # Définir la couleur noire (éteint) pour toutes les LEDs

    def flash(self, color, flash_count=3, wait_ms=200, brightness=255):
        """Fait clignoter toutes les LEDs avec une couleur donnée."""
        time.sleep(wait_ms / 1000.0)
        for _ in range(flash_count):
            self.set_all_del_color(color, brightness=brightness)
            time.sleep(wait_ms / 1000.0)
            self.eteindre()
            time.sleep(wait_ms / 1000.0)

    def heartbeat(self, color, beat_count=3, wait_ms=100):
        """Effet de battement de cœur avec une couleur donnée."""
        for _ in range(beat_count):
            for brightness in range(0, 256, 15):
                self.set_all_del_color(color, brightness=brightness)
                time.sleep(wait_ms / 1000.0)

            for brightness in range(255, -1, -15):
                self.set_all_del_color(color, brightness=brightness)
                self.strip.show()
                time.sleep(wait_ms / 1000.0)

    def JayLeFou(self, color, beat_ms=100, flash_ms=200):
        """Effet personnalisé Jaylefou."""
        self.heartbeat(color, beat_count=10, wait_ms=beat_ms)
        self.flash(color, flash_count=2, wait_ms=flash_ms, brightness=128)
