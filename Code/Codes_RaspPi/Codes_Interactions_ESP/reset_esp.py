# Met la pin de reset des esp a 0
import RPi.GPIO as GPIO
import time
# Pin de reset pour les ESPs
reset_pin_RFID = 36
reset_pin_IO = 32
reset_pin_NEO = 22

# Correspondance des GPIO physiques pour les pins de reset
reset_GPIO_RFID = 16
reset_GPIO_IO = 12
reset_GPIO_NEO = 25

try:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(reset_pin_IO, GPIO.OUT)
    GPIO.setup(reset_pin_RFID, GPIO.OUT)
    GPIO.setup(reset_pin_NEO, GPIO.OUT)
    print("Pin de reset mise à LOW pour réinitialiser les ESPs.")
    while True:
        GPIO.output(reset_pin_IO, GPIO.LOW)
        GPIO.output(reset_pin_RFID, GPIO.LOW)
        GPIO.output(reset_pin_NEO, GPIO.LOW)
        time.sleep(1)  # Maintenir le reset pendant 1 seconde
        break
except Exception as e:
    print(f"Erreur lors de la configuration de la pin de reset: {e}")
except KeyboardInterrupt:
    print("Interruption par l'utilisateur. Nettoyage des GPIO.")
finally:
    GPIO.cleanup()