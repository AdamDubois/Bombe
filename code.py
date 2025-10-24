import time
from rpi_ws281x import PixelStrip, Color

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

def couleurUnique(strip, color, brightness=255):
    """Allume toutes les LEDs avec une couleur unique."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.setBrightness(brightness)
    strip.show()

def respire(strip, color, wait_ms=50, steps=5):
    """Effet de respiration avec une couleur donnée."""
    for brightness in range(0, 256, steps):
        strip.setBrightness(brightness)
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)
    for brightness in range(255, -1, -steps):
        strip.setBrightness(brightness)
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

def flash(strip, color, flash_count=3, wait_ms=200):
    """Fait clignoter toutes les LEDs avec une couleur donnée."""
    strip.setBrightness(255)
    couleurUnique(strip, Color(0, 0, 255))  # Éteindre avant de commencer
    time.sleep(wait_ms / 1000.0)
    for _ in range(flash_count):
        couleurUnique(strip, color)
        time.sleep(wait_ms / 1000.0)
        couleurUnique(strip, Color(0, 0, 0))  # Éteindre
        time.sleep(wait_ms / 1000.0)

def heartbeat(strip, color, beat_count=3, wait_ms=100):
    """Effet de battement de cœur avec une couleur donnée."""
    for _ in range(beat_count):
        for brightness in range(0, 256, 15):
            strip.setBrightness(brightness)
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
        for brightness in range(255, -1, -15):
            strip.setBrightness(brightness)
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)

def police(strip, color, flash_count=3, wait_ms=100):
    """Effet de lumière de police avec rouge et bleu."""
    strip.setBrightness(255)
    for _ in range(flash_count):
        couleurUnique(strip, Color(255, 0, 0))  # Rouge
        time.sleep(wait_ms / 1000.0)
        couleurUnique(strip, Color(0, 0, 255))  # Bleu
        time.sleep(wait_ms / 1000.0)
    couleurUnique(strip, Color(0, 0, 0))  # Éteindre à la fin

try:
    # couleurUnique(strip, Color(255, 255, 255))  # Allume toutes les LEDs en blanc
    # strip.setPixelColor(50, Color(255, 0, 0))  # Allume la première LED en rouge
    # strip.show()
    while True:
        # respire(strip, Color(255, 0, 0), wait_ms=150, steps=25)  # Effet de respiration en rouge
        police(strip, Color(255, 0, 0), flash_count=65000, wait_ms=2)  # Effet de lumière de police en rouge
        # flash(strip, Color(255, 0, 0), flash_count=5, wait_ms=300)  # Flash rouge 5 fois
        # heartbeat(strip, Color(255, 0, 0), beat_count=5, wait_ms=50)  # Effet de battement de cœur en rouge
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