import time
import board
import busio

# Configuration de l'UART
uart = busio.UART(board.TX, board.RX, baudrate=115200)

def write_uart():
    message = "Hello from ESP32!\n"
    uart.write(message.encode("utf-8"))  # Envoi des données
    print("Données envoyées :", message)
    time.sleep(1)  # Pause d'une seconde

def read_uart():
    data = uart.read(32)  # Lit jusqu'à 32 octets
    if data is not None:
        try:
            print("Données reçues :", data.decode("utf-8"))  # Décodage en UTF-8
            return data.decode("utf-8")
        except UnicodeError:
            # En cas d'erreur de décodage, retourner None ou une chaîne vide
            print("Erreur de décodage UTF-8, données ignorées")
            return None
    return None