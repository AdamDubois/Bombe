import time
import neopixel
import Config

class DEL:
    def __init__(self, pin=Config.LED_STRIP_PIN, led_count=Config.LED_STRIP_COUNT, brightness=0.5):
        self.led_count = led_count

        # objet NeoPixel
        self.pixels = neopixel.NeoPixel(
            pin,
            led_count,
            brightness=brightness,
            auto_write=False,
            pixel_order=neopixel.GRB  # bande WS2812 standard
        )

    def set_all(self, color):
        for i in range(self.led_count):
            self.pixels[i] = color
        self.pixels.show()

    def eteindre(self):
        self.set_all((0, 0, 0))

    def flash(self, color, flash_count=1, wait_ms=200):
        for _ in range(flash_count):
            self.set_all(color)
            time.sleep(wait_ms / 1000)
            self.eteindre()
            time.sleep(wait_ms / 1000)

    def heartbeat(self, color, wait_ms=40):
        # Mémoriser la luminosité actuelle
        old_brightness = self.pixels.brightness
        
        # montée
        for b in range(0, 255, 10):
            self.pixels.brightness = b / 255
            self.set_all(color)
            time.sleep(wait_ms / 1000)

        # descente
        for b in range(255, -1, -10):
            self.pixels.brightness = b / 255
            self.set_all(color)
            time.sleep(wait_ms / 1000)

        # Restaurer la luminosité d'origine
        self.pixels.brightness = old_brightness

    def JayLeFou(self, color=(255, 0, 0)):
        # 10 battements rapides
        for _ in range(10):
            self.heartbeat(color)

        # Gros flash final
        self.flash(color, flash_count=2)