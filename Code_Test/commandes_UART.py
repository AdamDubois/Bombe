import serial
import time

# --- CONFIG --- #
# Modifie le port selon ton branchement :
# Par USB (câble direct) souvent : "/dev/ttyACM0" ou "/dev/ttyUSB0"
# Par GPIO hardware UART : "/dev/serial0" ou "/dev/ttyS0"
SERIAL_PORT = "/dev/serial0"
BAUDRATE = 115200

try:
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    print(f"Ouvert sur {SERIAL_PORT} ({BAUDRATE} bauds)")

    time.sleep(2)  # Laisse l'ESP32 booter et ouvrir Serial
    print("Prêt. Ctrl+C pour quitter.")

    while True:
        cmd = input("Commande à envoyer > ")
        # Ajoute le délimiteur \n attendu côté ESP32
        ser.write((cmd + "\n").encode('utf-8'))
        print("Envoyé.")
        # Option : lit la réponse éventuelle de l'ESP32
        # time.sleep(0.1)
        # if ser.in_waiting:
        #     print("Réponse:", ser.readline().decode().strip())

except KeyboardInterrupt:
    print("\nFin du script.")
except Exception as e:
    print("Erreur :", e)
finally:
    try:
        ser.close()
    except:
        pass