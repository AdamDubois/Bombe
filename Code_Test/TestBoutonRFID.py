import RPi.GPIO as GPIO
import time

from lib.mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

BUTTON_PIN = 16
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Appuyez sur le bouton (Ctrl+C pour quitter)")

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print("Bouton appuyé !")
            time.sleep(0.2)  # Anti-rebond (debounce)
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nArrêt.")
finally:
    GPIO.cleanup()