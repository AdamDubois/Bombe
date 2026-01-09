import Keypad as Keypad
import RPi.GPIO as GPIO

pad = Keypad.KeyPad()

try:
    while True:
        if pad.key_pressed is not None:
            print(f"Touche détectée dans le test: {pad.key_pressed}")
            pad.key_pressed = None  # Réinitialiser après la détection
except KeyboardInterrupt:
    print("Arrêt du test du pavé numérique.")
finally:
    pad.stop()