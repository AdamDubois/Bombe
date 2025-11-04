import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

POT_PIN = 16
GPIO.setup(POT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def read_potentiometer():
    # Lire la valeur du potentiomètre (0-1023)
    value = GPIO.input(POT_PIN)
    return value

try:
    while True:
        pot_value = read_potentiometer()
        print(f"Valeur du potentiomètre : {pot_value}")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\nArrêt.")
finally:
    GPIO.cleanup()