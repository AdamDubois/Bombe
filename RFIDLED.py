import RPi.GPIO as GPIO
from lib.mfrc522 import SimpleMFRC522
import class_DEL

reader = SimpleMFRC522()
LED = class_DEL.DEL()

try:
    try:
        while True:
            id, text = reader.read()
            print(id)
            print(text)
            print("Appliquer l'effet LED pour le tag lu...")
            print(type(text))
            LED.set_all_del_color("rouge")
            print("Effet LED appliqué pour le tag lu.")

    except KeyboardInterrupt:
        print("\nProgramme interrompu par l'utilisateur")
        LED.eteindre()
        LED.strip.show()
        print("LEDs éteintes - Nettoyage terminé")

except:
    pass

finally:
    GPIO.cleanup()