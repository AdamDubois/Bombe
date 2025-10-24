import class_DEL
from rpi_ws281x import Color

LED = class_DEL.DEL()

def main():
    """Programme principal pour tester les animations LED."""
    try:
        print('Contrôle de bande LED WS2812 - Appuyez Ctrl-C pour quitter.')
        while True:
            LED.JayLeFou("rouge")  # Effet personnalisé Jaylefou en rouge
    except KeyboardInterrupt:
        print("\nProgramme interrompu par l'utilisateur")
        LED.eteindre()
        LED.strip.show()
        print("LEDs éteintes - Nettoyage terminé")

if __name__ == '__main__':
    main()