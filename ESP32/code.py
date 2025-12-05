#!/usr/bin/env python
#coding: utf-8
"""
Fichier : code.py
Description: Code du ESP32-S3 Feather pour contrôler une bande de LEDs WS2812 via UART de manière asynchrone.
    - Utilise asyncio pour gérer la réception UART et les animations LED de manière non bloquante.
    - Supporte plusieurs animations prédéfinies et commandes de couleur.
    - Gère les interruptions et nettoie correctement les ressources à la fin.
    - Utilise une classe personnalisée pour gérer les LEDs.
"""
__author__ = "Adam Dubois et Jérémy Breault"
__version__ = "1.0.1"
__date__ = "2025-12-05"
__maintainer__ = "Adam Dubois"
__email__ = "adamdubois19@hotmail.com"
__status__ = "Production"


import asyncio
import lib.class_DEL as DEL
import lib.UART as UART


dict_Colors = {
        "RED": (255, 0, 0),
        "GREEN": (0, 255, 0),
        "BLUE": (0, 0, 255),
        "YELLOW": (255, 255, 0),
        "CYAN": (0, 255, 255),
        "MAGENTA": (255, 0, 255),
        "WHITE": (255, 255, 255),
    }

# Commandes spéciales pour couleurs fixes (sans animation)
dict_SolidColors = {
    "SOLID_RED": (255, 0, 0),
    "SOLID_GREEN": (0, 255, 0),
    "SOLID_BLUE": (0, 0, 255),
    "SOLID_WHITE": (255, 255, 255),
}

# Commandes rainbow
dict_RainbowCommands = {
    "RAINBOW": {"wait_ms": 20, "iterations": 5},
    "RAINBOW_FAST": {"wait_ms": 10, "iterations": 3},
    "RAINBOW_SLOW": {"wait_ms": 50, "iterations": 10},
    "RAINBOW_INFINITE": {"wait_ms": 20, "iterations": 999}
}

# Instance globale des LEDs
delstrip = DEL.DEL()

async def uart_handler():
    """Gestionnaire asynchrone pour la réception UART"""
    print("UART Handler démarré")
    while True:
        try:
            # Essayer d'abord la lecture par polling simple
            message = await UART.read_uart_polling()
            
            if message is not None:
                print(f"Message brut reçu: '{message}'")
                
                # Vérifier si c'est une commande rainbow
                if message in dict_RainbowCommands:
                    print(f"Commande Rainbow reçue: {message}")
                    params = dict_RainbowCommands[message]
                    await delstrip.start_rainbow_animation(params["wait_ms"], params["iterations"])
                    
                # Vérifier si c'est une commande d'animation JayLeFou
                elif message in dict_Colors:
                    print(f"Commande d'animation JayLeFou reçue: {message}")
                    # Démarrer l'animation asynchrone (interrompt la précédente)
                    await delstrip.start_animation(dict_Colors[message])
                    
                # Vérifier si c'est une commande de couleur fixe
                elif message in dict_SolidColors:
                    print(f"Commande couleur fixe reçue: {message}")
                    delstrip.set_solid_color(dict_SolidColors[message])
                    
                # Commande spéciale OFF
                elif message == "OFF":
                    print("Extinction des LEDs")
                    delstrip.set_solid_color((0, 0, 0))
                    
                else:
                    print(f"Commande inconnue: '{message}'")
                    print(f"Animations JayLeFou: {list(dict_Colors.keys())}")
                    print(f"Animations Rainbow: {list(dict_RainbowCommands.keys())}")
                    print(f"Couleurs fixes: {list(dict_SolidColors.keys())}")
            
            # Pause plus courte pour être plus réactif
            await asyncio.sleep(0.05)
            
        except Exception as e:
            print(f"Erreur dans uart_handler: {e}")
            await asyncio.sleep(0.1)

async def animation_manager():
    """Gestionnaire des animations LED"""
    while True:
        try:
            # Attendre que l'animation en cours se termine (si il y en a une)
            if delstrip.current_animation and not delstrip.current_animation.done():
                try:
                    await delstrip.current_animation
                    print("Animation terminée")
                except asyncio.CancelledError:
                    print("Animation annulée")
            
            await asyncio.sleep(0.1)
        except Exception as e:
            print(f"Erreur dans animation_manager: {e}")
            await asyncio.sleep(0.1)

async def main():
    """Fonction principale asynchrone"""
    print("Démarrage du système asyncio avec LEDs asynchrones...")
    print(f"UART configuré sur baudrate: {UART.uart.baudrate}")
    print("Commandes disponibles:")
    print(f"  Animations JayLeFou: {list(dict_Colors.keys())}")
    print(f"  Animations Rainbow: {list(dict_RainbowCommands.keys())}")
    print(f"  Couleurs fixes: {list(dict_SolidColors.keys())}")
    print("  OFF: éteint les LEDs")
    
    # Créer les tâches concurrentes
    tasks = [
        asyncio.create_task(uart_handler()),
        asyncio.create_task(animation_manager()),
    ]
    
    # Exécuter toutes les tâches en parallèle
    await asyncio.gather(*tasks)

################################
###   Programme principal    ###
################################

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Arrêt du programme")
    except Exception as e:
        print(f"Erreur fatale: {e}")