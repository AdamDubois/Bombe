from smbus2 import SMBus, i2c_msg      # Pour l'I2C (sudo pip install smbus2)
import time

# Adresse I2C de l'ESP32 (doit correspondre à SLAVE_ADDR dans ton Arduino)
ESP32_ADDR = 0x11  # (0x0a en hex, 10 en décimal)
mode = 0
I2C_BUS = 1        # Bus I2C habituels sur Pi (bus 1 sur la plupart des modèles)

bus = SMBus(I2C_BUS)

print("Envoi de message I2C vers ESP32, Ctrl+C pour quitter.")
try:
    while True:
        addr = input("Adresse I2C de l'ESP32 (en hex, ex: 0x10) ou Entrée pour utiliser 0x10: ")
        if addr.strip() != "":
            ESP32_ADDR = int(addr, 16)
        mode = input("Mode (0: Écriture, 1: Lecture): ")
        if mode.strip() == "0":
            # Mode écriture
            message = input("Message à envoyer (max 128 caractères): ")
            if len(message) > 128:
                print("Message trop long, maximum 128 caractères.")
                continue
            # Préparer les données à envoyer
            data = [ord(c) for c in message]
            try:
                i2c_msg_write = i2c_msg.write(ESP32_ADDR, data)
                bus.i2c_rdwr(i2c_msg_write)
                print("Message envoyé:", message)
            except Exception as e:
                print("Erreur d'écriture I2C:", e)
        elif mode.strip() == "1":
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
        else:
            print("Mode invalide, veuillez entrer 0 ou 1.")
            continue
except KeyboardInterrupt:
    print("\nFin du programme !")
finally:
    bus.close()