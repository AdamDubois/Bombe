import time
from rpi_ws281x import PixelStrip, Color

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

def flash(strip, color, flash_count=3, wait_ms=200, brightness=255):
    """Fait clignoter toutes les LEDs avec une couleur donnée."""
    time.sleep(wait_ms / 1000.0)
    for _ in range(flash_count):
        couleurUnique(strip, color, brightness=brightness)
        time.sleep(wait_ms / 1000.0)
        couleurUnique(strip, Color(0, 0, 0), brightness=brightness)  # Éteindre
        time.sleep(wait_ms / 1000.0,)

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

def jaylefou(strip, color, beat_ms=50, flash_ms=200):
    """Effet personnalisé Jaylefou."""
    heartbeat(strip, color, beat_count=10, wait_ms=beat_ms)
    flash(strip, color, flash_count=2, wait_ms=flash_ms, brightness=128)