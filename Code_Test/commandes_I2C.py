from smbus2 import SMBus, i2c_msg      # Pour l'I2C (sudo pip install smbus2)
import time

# Adresse I2C de l'ESP32 (doit correspondre à SLAVE_ADDR dans ton Arduino)
ESP32_ADDR = 0x10  # (0x0a en hex, 10 en décimal)
I2C_BUS = 1        # Bus I2C habituels sur Pi (bus 1 sur la plupart des modèles)

bus = SMBus(I2C_BUS)

print("Envoi de message I2C vers ESP32, Ctrl+C pour quitter.")
try:
    while True:
        addr = input("Adresse I2C de l'ESP32 (en hex, ex: 0x10) ou Entrée pour utiliser 0x10: ")
        if addr.strip() != "":
            ESP32_ADDR = int(addr, 16)
        try:
            strReceived = ""
            # Lecture de la réponse
            response = i2c_msg.read(ESP32_ADDR, 256)  # Lire jusqu'à 256 octets
            bus.i2c_rdwr(response)

            for value in response:
                if (value == 0x00):
                    break
                strReceived += chr(value)
            # Convertir la liste d'octets en chaîne
            print("Réponse reçue:", strReceived)
        except Exception as e:
            print("Erreur de lecture I2C:", e)
except KeyboardInterrupt:
    print("\nFin du programme !")
finally:
    bus.close()