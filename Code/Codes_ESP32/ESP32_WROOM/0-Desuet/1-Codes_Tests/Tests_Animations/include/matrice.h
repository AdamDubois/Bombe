#ifndef MATRICE_H
#define MATRICE_H

#include "config.h"

CRGB CRGBToCRGB(uint32_t c);
CRGB CRBGToCRGB(uint32_t c);
CRGB CGRBToCRGB(uint32_t c);
CRGB CBRGToCRGB(uint32_t c);
CRGB CBGRToCRGB(uint32_t c);
CRGB CGBRToCRGB(uint32_t c);

uint16_t getXYIndex(uint8_t x, uint8_t y);

void drawFrame(CRGB *leds, const uint32_t *frameData);

void drawChar(CRGB *leds, int16_t xPos, int16_t yPos, char c, CRGB color);

bool drawText(CRGB *leds, const char* text, CRGB color, int &scrollX);

#endif