#include "matrice.h"

/*
Brief : Cette fonction convertit une couleur au format 0xAARRGGBB en un objet CRGB de FastLED.
Paramètre : 
  - c - la couleur au format 0xAARRGGBB (Alpha, Rouge, Vert, Bleu)

Retour : 
  - Un objet CRGB correspondant à la couleur donnée. Si le canal alpha est égal à 0, la fonction retourne CRGB::Black (noir éteint)
*/
CRGB CRGBToCRGB(uint32_t c) {
  uint8_t a = (c >> 24) & 0xFF;
  if (a == 0) return CRGB::Black;

  uint8_t r = (c >> 16) & 0xFF;
  uint8_t g = (c >>  8) & 0xFF;
  uint8_t b = (c >>  0) & 0xFF;

  return CRGB(r, g, b);
}

/*
Brief : Cette fonction convertit une couleur au format 0xAARRBBGG en un objet CRGB de FastLED.
Paramètre : 
  - c - la couleur au format 0xAARRBBGG (Alpha, Rouge, Bleu, Vert)

Retour : 
  - Un objet CRGB correspondant à la couleur donnée. Si le canal alpha est égal à 0, la fonction retourne CRGB::Black (noir éteint)
*/
CRGB CRBGToCRGB(uint32_t c) {
  uint8_t a = (c >> 24) & 0xFF;
  if (a == 0) return CRGB::Black;

  uint8_t r = (c >> 16) & 0xFF;   // Rouge (0xAARRBBGG)
  uint8_t b = (c >>  8) & 0xFF;   // Bleu
  uint8_t g = (c >>  0) & 0xFF;   // Vert

  return CRGB(r, g, b);           // On remet dans l'ordre R-G-B pour FastLED
}

/*
Brief : Cette fonction convertit une couleur au format 0xAAGGRRBB en un objet CRGB de FastLED.
Paramètre : 
  - c - la couleur au format 0xAAGGRRBB (Alpha, Vert, Rouge, Bleu)

Retour : 
  - Un objet CRGB correspondant à la couleur donnée. Si le canal alpha est égal à 0, la fonction retourne CRGB::Black (noir éteint)
*/
CRGB CGRBToCRGB(uint32_t c) {
  uint8_t a = (c >> 24) & 0xFF;
  if (a == 0) return CRGB::Black;

  uint8_t g = (c >> 16) & 0xFF;   // Vert (0xAAGGRRBB)
  uint8_t r = (c >>  8) & 0xFF;   // Rouge 
  uint8_t b = (c >>  0) & 0xFF;   // Bleu

  return CRGB(r, g, b);           // On remet dans l'ordre R-G-B pour FastLED
}

/*
Brief : Cette fonction convertit une couleur au format 0xAABBRRGG en un objet CRGB de FastLED.
Paramètre : 
  - c - la couleur au format 0xAABBRRGG (Alpha, Bleu, Rouge, Vert)

Retour : 
  - Un objet CRGB correspondant à la couleur donnée. Si le canal alpha est égal à 0, la fonction retourne CRGB::Black (noir éteint)
*/
CRGB CBRGToCRGB(uint32_t c) {
  uint8_t a = (c >> 24) & 0xFF;
  if (a == 0) return CRGB::Black;

  uint8_t b = (c >> 16) & 0xFF;   // Bleu (0xAABBRRGG)
  uint8_t r = (c >>  8) & 0xFF;   // Rouge 
  uint8_t g = (c >>  0) & 0xFF;   // Vert

  return CRGB(r, g, b);           // On remet dans l'ordre R-G-B pour FastLED
}

/*
Brief : Cette fonction convertit une couleur au format 0xAABBGGRR en un objet CRGB de FastLED.
Paramètre : 
  - c - la couleur au format 0xAABBGGRR (Alpha, Bleu, Vert, Rouge)

Retour :
  - Un objet CRGB correspondant à la couleur donnée. Si le canal alpha est égal à 0, la fonction retourne CRGB::Black (noir éteint)
*/
CRGB CBGRToCRGB(uint32_t c) {
  uint8_t a = (c >> 24) & 0xFF;
  if (a == 0) return CRGB::Black;

  uint8_t b = (c >> 16) & 0xFF;   // Bleu (0xAABBGGRR)
  uint8_t g = (c >>  8) & 0xFF;   // Vert 
  uint8_t r = (c >>  0) & 0xFF;   // Rouge

  return CRGB(r, g, b);           // On remet dans l'ordre R-G-B pour FastLED
}

/*
Brief : Cette fonction convertit une couleur au format 0xAAGGBBRR en un objet CRGB de FastLED.
Paramètre : 
  - c - la couleur au format 0xAAGGBBRR (Alpha, Vert, Bleu, Rouge)

Retour : 
  - Un objet CRGB correspondant à la couleur donnée. Si le canal alpha est égal à 0, la fonction retourne CRGB::Black (noir éteint)
*/
CRGB CGBRToCRGB(uint32_t c) {
  uint8_t a = (c >> 24) & 0xFF;
  if (a == 0) return CRGB::Black;

  uint8_t g = (c >> 16) & 0xFF;   // Vert (0xAAGGBBRR)
  uint8_t b = (c >>  8) & 0xFF;   // Bleu 
  uint8_t r = (c >>  0) & 0xFF;   // Rouge

  return CRGB(r, g, b);           // On remet dans l'ordre R-G-B pour FastLED
}

// Mapping serpentin par colonnes (validé sur votre matrice)
/*
Brief : Cette fonction calcule l'index dans le tableau de LEDs à partir des coordonnées x et y sur la matrice, en tenant compte du mapping en serpentin par colonnes.
Paramètre : 
  - x : la coordonnée x (colonne) sur la matrice (0 à WIDTH-1)
  - y : la coordonnée y (ligne) sur la matrice (0 à HEIGHT-1)

  Retour :
  - L'index dans le tableau de LEDs correspondant à la position (x, y)
*/
uint16_t getXYIndex(uint8_t x, uint8_t y) {
  if (x >= WIDTH || y >= HEIGHT) return 0;
  if ((x & 1) == 0) return x * HEIGHT + y;        // colonnes paires : haut → bas
  return x * HEIGHT + (HEIGHT - 1 - y);           // colonnes impaires : bas → haut
}

/*
Brief : Cette fonction dessine une frame complète sur la matrice à partir d'un tableau de données de couleurs au format 0xAABBGGRR. SI la couleur n'est pas en format 0xAABBGGRR, il suffit de changer la fonction de conversion utilisée (ex : CRGBToCRGB, CRBGToCRGB, etc.)

Important : La frame est uniquement mise en mémoire dans la matrice. Il faut appeler FastLED.show() après pour afficher la frame.
Paramètre :
  - leds : le tableau de LEDs à mettre à jour
  - frameData : un tableau de couleurs au format 0xAABBGGRR représentant la frame à dessiner, de taille WIDTH * HEIGHT
*/
void drawFrame(CRGB *leds, const uint32_t *frameData) {
  for (uint8_t y = 0; y < HEIGHT; y++) {
    for (uint8_t x = 0; x < WIDTH; x++) {
      uint16_t indexCouleur = (uint16_t)y * WIDTH + x;
      uint16_t indexDel = getXYIndex(x, y);
      leds[indexDel] = CBGRToCRGB(frameData[indexCouleur]);
    }
  }
}

/*
Brief : Cette fonction dessine un caractère à une position donnée sur la matrice, en utilisant une couleur spécifiée. Le caractère est défini dans la police Font5x7, et la fonction utilise le mapping en serpentin par colonnes pour placer les LEDs correctement.

Important : Le caractère est uniquement mis en mémoire dans la matrice. Il faut appeler FastLED.show() après pour afficher le caractère.
Paramètre :
  - leds : le tableau de LEDs à mettre à jour
  - xPos : la position x (colonne) où dessiner le caractère (0 à WIDTH-1)
  - yPos : la position y (ligne) où dessiner le caractère (0 à HEIGHT-1)
  - c : le caractère à dessiner (doit être entre ' ' (32) et '~' (127))
  - color : la couleur du caractère au format CRGB
*/
void drawChar(CRGB *leds, int16_t xPos, int16_t yPos, char c, CRGB color) {
  if (c < 32 || c > 127) return;
  uint8_t charIndex = c - 32;

  for (uint8_t col = 0; col < 5; col++) {  // col = colonne de 0 (gauche) à 4 (droite)
    uint8_t columnData = pgm_read_byte(&Font5x7[charIndex * 5 + col]);

    for (uint8_t row = 0; row < 8; row++) {  // row = ligne de haut (0) à bas (7)
      if (columnData & (1 << row)) {         // bit 0 = haut, bit 7 = bas (inverse si besoin)
        int16_t screenX = xPos + col;
        int16_t screenY = yPos + row;
        if (screenX >= 0 && screenX < WIDTH && screenY >= 0 && screenY < HEIGHT) {
          leds[getXYIndex(screenX, screenY)] = color;
        }
      }
    }
  }
}

/*
Brief : Cette fonction dessine un texte défilant sur la matrice, en utilisant une couleur spécifiée. Le texte est défini par une chaîne de caractères, et la fonction utilise le mapping en serpentin par colonnes pour placer les LEDs correctement. La position de départ du texte est contrôlée par la variable scrollX, qui doit être initialisée à WIDTH pour commencer le défilement depuis la droite.

Important : Le texte est uniquement mis en mémoire dans la matrice. Il faut appeler FastLED.show() après pour afficher le texte.
Paramètre :
  - leds : le tableau de LEDs à mettre à jour
  - text : la chaîne de caractères à faire défiler (doit être composée de caractères entre ' ' (32) et '~' (127))
  - color : la couleur du texte au format CRGB
  - scrollX : une référence à la variable contrôlant la position horizontale du texte, qui doit être initialisée à WIDTH pour commencer le défilement depuis la droite. La fonction met à jour scrollX pour faire défiler le texte, et retourne true lorsque le texte a complètement défilé et que scrollX peut être réinitialisé à la valeur de départ.

  Retour :
  - true si le texte a complètement défilé (scrollX est réinitialisé à la valeur de départ)
  - false si le texte est encore en train de défiler
*/
bool drawText(CRGB *leds, const char* text, CRGB color, int &scrollX) {
  FastLED.clear();

  int textLen = strlen(text);
  int charWidth = 6;  // 5 pixels + 1 espace

  for (int i = 0; i < textLen; i++) {
    int charX = scrollX + i * charWidth;
    int charY = (HEIGHT - 7) / 2;  // Centrage vertical (≈0 ou 1)

    drawChar(leds, charX, charY, text[i], color);  // Utilise la couleur spécifiée
  }

  scrollX--;

  if (scrollX < - (textLen * charWidth)) {
    scrollX = WIDTH;  // Réinitialise la position de départ pour le défilement
    return true;  // Le texte a complètement défilé, on peut réinitialiser scrollX à la valeur de départ
  }

  return false;
}