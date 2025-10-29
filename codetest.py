import time
from lib.rpi_ws281x_1_1_3.neopixel import Adafruit_NeoPixel as PixelStrip, Color

# Configuration des LEDs WS2812
LED_COUNT = 75          # Nombre de LEDs dans la bande (ajustez selon votre bande)
LED_PIN = 18           # Pin GPIO utilisé pour contrôler les LEDs (doit être PWM)
LED_FREQ_HZ = 800000   # Fréquence du signal LED en hertz (800khz)
LED_DMA = 10           # Canal DMA à utiliser pour générer le signal (essayez 10)
LED_BRIGHTNESS = 255   # Luminosité des LEDs (0-255)
LED_INVERT = False     # True pour inverser le signal (quand on utilise un transistor NPN)
LED_CHANNEL = 0        # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Créer l'objet PixelStrip
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

# Initialiser la bibliothèque (doit être appelé une fois avant les autres fonctions)
strip.begin()

def colorWipe(strip, color, wait_ms=50):
    """Allume les pixels un par un avec la couleur spécifiée."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Animation théâtre - pixels allumés tous les 3 pixels."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)

def wheel(pos):
    """Génère des couleurs arc-en-ciel sur 0-255."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Dessine un arc-en-ciel sur tous les pixels."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Dessine un arc-en-ciel uniformément réparti sur tous les pixels."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel(((i * 256 // strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Animation théâtre arc-en-ciel."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)

try:
    print('Contrôle de bande LED WS2812 - Appuyez Ctrl-C pour quitter.')
    while True:
        print('Animation balayage de couleurs...')
        colorWipe(strip, Color(255, 0, 0))  # Rouge
        colorWipe(strip, Color(0, 255, 0))  # Vert
        colorWipe(strip, Color(0, 0, 255))  # Bleu
        
        print('Animation théâtre...')
        theaterChase(strip, Color(127, 127, 127))  # Blanc
        theaterChase(strip, Color(127, 0, 0))      # Rouge
        theaterChase(strip, Color(0, 0, 127))      # Bleu
        
        print('Animations arc-en-ciel...')
        rainbow(strip)
        rainbowCycle(strip)
        theaterChaseRainbow(strip)

except KeyboardInterrupt:
    print("\nProgramme interrompu par l'utilisateur")
    # Éteindre toutes les LEDs
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
    print("LEDs éteintes - Nettoyage terminé")