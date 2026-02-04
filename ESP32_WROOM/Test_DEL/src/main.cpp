#include <Arduino.h>
#include <Adafruit_NeoPixel.h>

// Which pin on the ESP32 is connected to the NeoPixels? In this case, pin 4
#define LED1_PIN 9
// How many NeoPixels are attached to the Arduino?
#define LED1_COUNT 40
// Declare our NeoPixel strip object:

#define LED2_PIN 8
#define LED2_COUNT 40
#define LED3_PIN 5
#define LED3_COUNT 40
#define LED4_PIN 4
#define LED4_COUNT 40
#define LED5_PIN 0
#define LED5_COUNT 40
#define LED6_PIN 1
#define LED6_COUNT 9
#define LED7_PIN 3
#define LED7_COUNT 256

// Tableau des objets NeoPixel
Adafruit_NeoPixel strips[] = {
  Adafruit_NeoPixel(LED1_COUNT, LED1_PIN, NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(LED2_COUNT, LED2_PIN, NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(LED3_COUNT, LED3_PIN, NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(LED4_COUNT, LED4_PIN, NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(LED5_COUNT, LED5_PIN, NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(LED6_COUNT, LED6_PIN, NEO_GRB + NEO_KHZ800),
  Adafruit_NeoPixel(LED7_COUNT, LED7_PIN, NEO_GRB + NEO_KHZ800),
};

const uint8_t NUM_STRIPS = sizeof(strips) / sizeof(strips[0]);

uint32_t colors[NUM_STRIPS] = {
    strips[0].Color(255, 255, 255), // blanc
    strips[0].Color(255, 0, 0),     // rouge
    strips[0].Color(0, 0, 255),     // bleu
    strips[0].Color(0, 255, 0),     // vert
    strips[0].Color(255, 255, 0),   // jaune
    strips[0].Color(255, 0, 255),   // magenta
    strips[0].Color(0, 255, 255),   // cyan
  };

const uint8_t NUM_COLORS = sizeof(colors) / sizeof(colors[0]);

int colorIndex[NUM_STRIPS] = {
    0, 
    1, 
    2, 
    3, 
    4, 
    5, 
    6
  };


// put function declarations here:
void initNeoPixels();

void setup() {
  // put your setup code here, to run once:
  initNeoPixels();
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(250);
  for (uint8_t i = 0; i < NUM_STRIPS; i++) {
    strips[i].fill(colors[colorIndex[i]]);
    strips[i].show();
    colorIndex[i]++;
    if (colorIndex[i] >= NUM_COLORS) {
      colorIndex[i] = 0;
    }
  }
}

// put function definitions here:
void initNeoPixels() 
{
  for (uint8_t i = 0; i < NUM_STRIPS; i++) {
    strips[i].begin();           // INITIALIZE NeoPixel strip object (REQUIRED)
    strips[i].show();            // Turn OFF all pixels ASAP
    strips[i].setBrightness(100); // Set BRIGHTNESS to about 1/5 (max = 255)
  }
}