#include "config.h"

CRGB leds[NUM_LEDS];

int g_animation = 0;
int g_scrollX = WIDTH;
int g_index_r = 0;
int g_index_g = -1;
int g_index_b = -2;

void setup() {
  Serial.begin(9600);
  FastLED.addLeds<WS2815, DATA_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(255);
  FastLED.clear();
  FastLED.show();
}

void loop() {
  // if (random(0, 100) < 5) {
  //   g_animation = random(0, 4);
  //   FastLED.clear();
  //   FastLED.show();

  //   int g_scrollX = WIDTH;
  //   int g_index_r = 0;
  //   int g_index_g = -1;
  //   int g_index_b = -2;

  //   // Serial.print("Animation: ");
  //   // Serial.println(g_animation);

  //   // Serial.print("g_scrollX: ");
  //   // Serial.println(g_scrollX);

  //   // Serial.print("g_index_r: ");
  //   // Serial.println(g_index_r);
  //   // Serial.print("g_index_g: ");
  //   // Serial.println(g_index_g);
  //   // Serial.print("g_index_b: ");
  //   // Serial.println(g_index_b);

  //   delay(1000);
  // }

  if (g_animation == 0) {
    for (int i = 0; i < NUM_LEDS; i++) {
      leds[i] = CRGB(255, 0, 255); // Magenta
    }
    FastLED.show();
    delay(1000);

    g_animation = 1;
    FastLED.clear();
    FastLED.show();
  }

// ----------------------------------------------------------------------------------------------------------

  if (g_animation == 1) {
    static uint8_t frame = 0;
    static uint32_t last = 0;

    const uint16_t frameDelayMs = 120;   // Vitesse d'animation (ms par frame)

    uint32_t now = millis();
    if (now - last >= frameDelayMs) {
      last = now;

      drawFrame(leds, help_animation_data[frame++]);
      FastLED.show();

      if (frame >= HELP_ANIMATION_FRAME_COUNT) {
        frame = 0;
        g_animation = 2;
        FastLED.clear();
        FastLED.show();
      }
    }
  }

// ----------------------------------------------------------------------------------------------------------

  if (g_animation == 2) {
    const char* text = "HELLO WORLD 123 !";

    if (drawText(leds, text, CRGB::Cyan, g_scrollX)) {
      g_animation = 3;
      FastLED.clear();
      FastLED.show();
    }
    else {
      FastLED.show();
      delay(50);
    }
  }

// ----------------------------------------------------------------------------------------------------------

  if (g_animation == 3) {
    if (g_index_b >= NUM_LEDS ) {
      g_index_r = 0;
      g_index_g = -1;
      g_index_b = -2;

      g_animation = 0;
      FastLED.clear();
      FastLED.show();
    }
    else {
      fill_solid(leds, NUM_LEDS, CRGB::Black);
      if (g_index_r >= 0 && g_index_r < NUM_LEDS) leds[g_index_r] = CRGB::Red;
      if (g_index_g >= 0 && g_index_g < NUM_LEDS) leds[g_index_g] = CRGB::Green;
      if (g_index_b >= 0 && g_index_b < NUM_LEDS) leds[g_index_b] = CRGB::Blue;
      FastLED.show();

      g_index_r++;
      g_index_g++;
      g_index_b++;

      delay(100);
    }
  }

// ----------------------------------------------------------------------------------------------------------

  // // Effet course Hotwheel : 6 voitures, vitesses variables et lentes
  // static const int numCars = 6;
  // static int carPos[numCars] = {0};
  // static float carSpeed[numCars] = {0};
  // static float carSpeedTarget[numCars] = {0};
  // static CRGB carColor[numCars] = {
  //   CRGB(255,0,0),     // rouge
  //   CRGB(0,255,0),     // vert
  //   CRGB(0,0,255),     // bleu
  //   CRGB(255,255,0),   // jaune
  //   CRGB(255,0,255),   // magenta
  //   CRGB(0,255,255)    // cyan
  // };
  // static int carLaps[numCars] = {0};
  // static int lastCarPos[numCars] = {0};
  // static bool raceFinished = false;
  // static int winnerIdx = -1;
  // static uint32_t lastRace = 0;
  // static uint32_t raceEndTime = 0;
  // const int raceInterval = 60; // ms entre chaque frame (plus lent)
  // static bool raceInit = false;

  // if (!raceInit) {
  //   for (int i = 0; i < numCars; i++) {
  //     carPos[i] = 0;
  //     carSpeed[i] = random(1, 6);
  //     carSpeedTarget[i] = random(1, 6);
  //     carLaps[i] = 0;
  //     lastCarPos[i] = 0;
  //   }
  //   // Boost magenta (voiture 4)
  //   carSpeed[4] += 0.1;
  //   carSpeedTarget[4] += 0.1;
  //   raceFinished = false;
  //   winnerIdx = -1;
  //   raceEndTime = 0;
  //   raceInit = true;
  // }

  // if (!raceFinished && millis() - lastRace > raceInterval) {
  //   lastRace = millis();
  //   fill_solid(leds, NUM_LEDS, CRGB::Black);
  //   for (int i = 0; i < numCars; i++) {
  //     // chaque voiture est un segment de 3 LEDs
  //     for (int j = 0; j < 3; j++) {
  //       int pos = (carPos[i] + j) % NUM_LEDS;
  //       leds[pos] = carColor[i];
  //     }
  //     // Variation de vitesse : cible change toutes les 2 secondes
  //     if (random(0, 100) < 5) {
  //       carSpeedTarget[i] = random(1, 6);
  //       if (i == 4) carSpeedTarget[i] += 0.1; // boost magenta
  //     }
  //     // Vitesse évolue doucement vers la cible
  //     if (carSpeed[i] < carSpeedTarget[i]) carSpeed[i] += 0.1;
  //     else if (carSpeed[i] > carSpeedTarget[i]) carSpeed[i] -= 0.1;
  //     // Avance
  //     int newPos = (int)(carPos[i] + carSpeed[i]) % NUM_LEDS;
  //     // Détection de passage ligne départ (position 0)
  //     if (lastCarPos[i] > newPos && newPos < 3) {
  //       carLaps[i]++;
  //       if (carLaps[i] >= 3 && !raceFinished) {
  //         winnerIdx = i;
  //         raceFinished = true;
  //         raceEndTime = millis();
  //       }
  //     }
  //     carPos[i] = newPos;
  //     lastCarPos[i] = newPos;
  //   }
  //   FastLED.show();
  // }

  // // Affiche la couleur du gagnant et relance la course après 5 secondes
  // if (raceFinished && winnerIdx >= 0) {
  //   fill_solid(leds, NUM_LEDS, carColor[winnerIdx]);
  //   FastLED.show();
  //   if (millis() - raceEndTime > 5000) {
  //     raceInit = false;
  //   }
  // }
}