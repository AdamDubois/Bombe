import RPi.GPIO as GPIO
from lib.mfrc522 import SimpleMFRC522
import class_DEL

GPIO.cleanup()

reader = SimpleMFRC522()
LED = class_DEL.DEL()

try:
    try:
        while True:
            id, text = reader.read()
            text = text.strip() # Nettoyer les espaces blancs
            print(id)
            print(text)
            LED.JayLeFou(text)
    except KeyboardInterrupt:
        print("\nProgramme interrompu par l'utilisateur")
        LED.eteindre()
        LED.strip.show()
        print("LEDs éteintes - Nettoyage terminé")

except:
    pass

finally:
    GPIO.cleanup()