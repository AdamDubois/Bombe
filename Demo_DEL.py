import class_DEL

LED = class_DEL.DEL()

def main():
    """Programme principal pour tester les animations LED."""
    try:
        print('Contrôle de bande LED WS2812 - Appuyez Ctrl-C pour quitter.')
        while True:
            pass  # Le code d'animation peut être ajouté ici
    except KeyboardInterrupt:
        print("\nProgramme interrompu par l'utilisateur")
        LED.eteindre()
        print("LEDs éteintes - Nettoyage terminé")

if __name__ == '__main__':
    main()