# ESP32 RFID - Lecteur Multi-MFRC522

Module ESP32-C3 configuré en esclave I2C pour la lecture de plusieurs lecteurs RFID MFRC522.

## Description

Ce projet utilise 4 lecteurs RFID MFRC522 connectés à un ESP32-C3. L'ESP32 agit comme esclave I2C et, sur demande du maître, scanne les lecteurs et renvoie les UIDs des cartes détectées au format JSON.

## Matériel requis

- ESP32-C3-DevKitC-02
- 4 lecteurs MFRC522
- Cartes RFID compatibles

## Câblage

### Bus I2C (vers le maître)

| Signal | GPIO |
|--------|------|
| SDA    | 6    |
| SCL    | 7    |

### Bus SPI (vers les MFRC522)

| Signal | GPIO |
|--------|------|
| SCK    | 4    |
| MOSI   | 10   |
| MISO   | 5    |
| RST    | 0    |

### Slave Select (SS) par lecteur

| Lecteur | GPIO |
|---------|------|
| SS_1    | 3    |
| SS_2    | 1    |
| SS_3    | 18   |
| SS_4    | 19   |

## Configuration

Tous les paramètres sont dans `include/config.h` :

- `SLAVE_ADDR` : Adresse I2C de l'esclave (défaut: `0x11`)
- `NR_OF_READERS` : Nombre de lecteurs connectés
- `DEBUG_MODE` : Active/désactive les logs série
- Broches I2C, SPI et SS

### Ajout de lecteurs supplémentaires

1. Définir `NR_OF_READERS` dans `config.h` au nombre désiré (max 8).
2. Ajouter les définitions de broches SS supplémentaires dans `config.h`.
3. Ajouter les broches SS supplémentaires dans le tableau `ssPins[]` dans `config.h`.

## Format de sortie JSON

```json
{N:"RFID",R0:"AAAAAAAA",R1:"NONE",R2:"AAAAAAAA",R3:"NONE"}
```

- `N` : Nom de l'ESP32
- `R0`-`R3` : UID de chaque lecteur (`NONE` si aucune carte)

## Limitations
- Le ESP32, sans modification, ne peut pas envoyer plus de 128 octets en une seule transmission I2C. Si le JSON dépasse cette taille, il sera tronqué. Le nombre maximal de lecteurs est donc limité en conséquence à 8 : {N:"RFID",R0:"AAAAAAAA",R1:"AAAAAAAA",R2:"AAAAAAAA",R3:"AAAAAAAA",R4:"AAAAAAAA",R5:"AAAAAAAA",R6:"AAAAAAAA",R7:"AAAAAAAA"} (122 octets).

## Dépendances

- [MFRC522](https://github.com/miguelbalboa/rfid) v1.4.12
- [ArduinoJson](https://github.com/bblanchon/ArduinoJson) v7.4.2

## Auteur

Adam Dubois - 2026