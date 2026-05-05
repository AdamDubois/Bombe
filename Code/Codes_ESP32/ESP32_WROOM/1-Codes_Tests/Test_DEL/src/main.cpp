#include <FastLED.h>

// Configuration de la seule bande conservée
#define LED0_PIN      9
#define LED0_COUNT    60

#define LED1_PIN      10
#define LED1_COUNT    60

#define LED2_PIN      5
#define LED2_COUNT    60

#define LED3_PIN      4
#define LED3_COUNT    60

#define LED4_PIN      3
#define LED4_COUNT    60

#define LED5_PIN      1
#define LED5_COUNT    60

#define LED6_PIN      0
#define LED6_COUNT    60

#define LED7_PIN      18
#define LED7_COUNT    60


CRGB leds0[LED0_COUNT];
CRGB leds1[LED1_COUNT];
CRGB leds2[LED2_COUNT];
CRGB leds3[LED3_COUNT];
CRGB leds4[LED4_COUNT];
CRGB leds5[LED5_COUNT];
CRGB leds6[LED6_COUNT];
CRGB leds7[LED7_COUNT];

void setup() {
  Serial.begin(9600);
  FastLED.addLeds<WS2815, LED0_PIN, GRB>(leds0, LED0_COUNT);  // WS2815, ordre GRB standard
  FastLED.addLeds<WS2815, LED1_PIN, GRB>(leds1, LED1_COUNT);  // WS2815, ordre GRB standard
  FastLED.addLeds<WS2815, LED2_PIN, GRB>(leds2, LED2_COUNT);  // WS2815, ordre GRB standard
  FastLED.addLeds<WS2815, LED3_PIN, GRB>(leds3, LED3_COUNT);  // WS2815, ordre GRB standard
  FastLED.addLeds<WS2815, LED4_PIN, GRB>(leds4, LED4_COUNT);  // WS2815, ordre GRB standard
  FastLED.addLeds<WS2815, LED5_PIN, GRB>(leds5, LED5_COUNT);  // WS2815, ordre GRB standard
  FastLED.addLeds<WS2815, LED6_PIN, GRB>(leds6, LED6_COUNT);  // WS2815, ordre GRB standard
  FastLED.addLeds<WS2815, LED7_PIN, GRB>(leds7, LED7_COUNT);  // WS2815, ordre GRB standard
  FastLED.setBrightness(255);  // 0-255, ajuste selon ton alimentation
  FastLED.clear();
  FastLED.show();
}

void loop() {
  fill_solid(leds0, LED0_COUNT, CRGB::White); // Allume en blanc
  FastLED.show();
  Serial.println("Bande 0 allumée");
  sleep(1); // Attendre 1 seconde
  fill_solid(leds1, LED1_COUNT, CRGB::White); // Allume en blanc
  FastLED.show();
  Serial.println("Bande 1 allumée");
  sleep(1); // Attendre 1 seconde
  fill_solid(leds2, LED2_COUNT, CRGB::White); // Allume en blanc
  FastLED.show();
  Serial.println("Bande 2 allumée");
  sleep(1); // Attendre 1 seconde
  fill_solid(leds3, LED3_COUNT, CRGB::White); // Allume en blanc
  FastLED.show();
  Serial.println("Bande 3 allumée");
  sleep(1); // Attendre 1 seconde
  fill_solid(leds4, LED4_COUNT, CRGB::White); // Allume en blanc
  FastLED.show();
  Serial.println("Bande 4 allumée");
  sleep(1); // Attendre 1 seconde
  fill_solid(leds5, LED5_COUNT, CRGB::White); // Allume en blanc
  FastLED.show();
  Serial.println("Bande 5 allumée");
  sleep(1); // Attendre 1 seconde
  fill_solid(leds6, LED6_COUNT, CRGB::White); // Allume en blanc
  FastLED.show();
  Serial.println("Bande 6 allumée");
  sleep(1); // Attendre 1 seconde
  fill_solid(leds7, LED7_COUNT, CRGB::White); // Allume en blanc
  FastLED.show();
  Serial.println("Bande 7 allumée");
  sleep(1); // Attendre 1 seconde
  FastLED.clear();
  FastLED.show();
}