import serial
import time
import os

# Configuration du port série
# Sur Raspberry Pi, utilisez /dev/serial0 qui pointe vers le bon port UART
port = '/dev/serial0'

# Vérifier si le port existe et est accessible
if not os.path.exists(port):
    print(f"Erreur: Le port {port} n'existe pas")
    print("Ports série disponibles:")
    os.system("ls -l /dev/tty* | grep -E '(ttyS|serial|ttyAMA)'")
    exit(1)

try:
    uart = serial.Serial(
        port=port,
        baudrate=9600,        # Définissez le débit en bauds
        timeout=1             # Timeout pour la lecture/écriture
    )
except PermissionError as e:
    print(f"Erreur de permission: {e}")
    print(f"Solutions possibles:")
    print(f"1. Exécuter avec sudo: sudo python3 {__file__}")
    print(f"2. Ajouter votre utilisateur au groupe dialout: sudo usermod -a -G dialout $USER")
    print(f"3. Modifier les permissions: sudo chmod 666 {port}")
    exit(1)
except serial.SerialException as e:
    print(f"Erreur série: {e}")
    exit(1)

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