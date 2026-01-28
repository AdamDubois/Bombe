import smbus2      # Pour l'I2C (sudo pip install smbus2)
import time

# Adresse I2C de l'ESP32 (doit correspondre à SLAVE_ADDR dans ton Arduino)
ESP32_ADDR = 0x10  # (0x0a en hex, 10 en décimal)
I2C_BUS = 1        # Bus I2C habituels sur Pi (bus 1 sur la plupart des modèles)

bus = smbus2.SMBus(I2C_BUS)

print("Envoi de message I2C vers ESP32, Ctrl+C pour quitter.")
try:
    while True:
        addr = input("Adresse I2C de l'ESP32 (en hex, ex: 0x10) ou Entrée pour utiliser 0x10: ")
        if addr.strip() != "":
            ESP32_ADDR = int(addr, 16)
        user_msg = input("Message à envoyer (texte, ex: TEST): ")
        # On convertit la chaîne en liste d'octets (bytearray), limite: 32 à 128 octets selon le MCU
        data = bytearray(user_msg, "utf-8")
        # Envoi sur le bus (tous les octets sauf \0 final)
        for i in range(0, len(data), 30):  # Envoie par paquets de 30 pour être compatible
            bus.write_i2c_block_data(ESP32_ADDR, 0, list(data[i:i+30]))
            time.sleep(0.05)  # Laisse le temps au microcontrôleur d'avaler le block
        print("Envoyé!")
        # On attend une réponse
        time.sleep(0.1)  # Petit délai avant de lire la réponse
        try:
            # Lecture de la réponse (max 32 octets)
            response = bus.read_i2c_block_data(ESP32_ADDR, 0, 32)
            # Convertir la liste d'octets en chaîne
            response_str = ''.join([chr(b) for b in response if b != 0])
            print("Réponse reçue:", response_str)
        except Exception as e:
            print("Erreur de lecture I2C:", e)
except KeyboardInterrupt:
    print("\nFin du programme !")
finally:
    bus.close()