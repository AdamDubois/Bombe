import serial
import time

# Configuration du port série
uart = serial.Serial(
    port='/dev/ttyS0',  # Utilisez /dev/serial0 pour GPIO 14 et 15
    baudrate=9600,        # Définissez le débit en bauds
    timeout=1             # Timeout pour la lecture/écriture
)

try:
    # Envoyer un message
    message = "Bonjour, UART !\n"
    uart.write(message.encode('utf-8'))
    print(f"Message envoyé : {message}")

    # Lire une réponse (si nécessaire)
    time.sleep(1)  # Attendre un peu pour recevoir une réponse
    if uart.in_waiting > 0:
        response = uart.read(uart.in_waiting).decode('utf-8')
        print(f"Réponse reçue : {response}")

except Exception as e:
    print(f"Erreur : {e}")

finally:
    # Fermer le port série
    uart.close()