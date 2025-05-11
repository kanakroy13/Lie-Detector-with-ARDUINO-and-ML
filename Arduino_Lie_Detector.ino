#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"

#define LM35_PIN A0     // LM35 Temperature Sensor
#define GSR_PIN A1      // GSR Sensor
#define PIEZO_PIN A2    // Piezoelectric Sensor

MAX30105 particleSensor;

const byte RATE_SIZE = 4;
byte rates[RATE_SIZE];
byte rateSpot = 0;
long lastBeat = 0;

float beatsPerMinute = 0;
int beatAvg = 0;
int rapidChanges = 0;
float prevBPM = 0;
float stableBPM = 0;
byte stableCounter = 0;

void setup() {
  Serial.begin(9600);
  while (!Serial);

  Serial.println("Initializing sensors...");

  if (!particleSensor.begin(Wire, I2C_SPEED_STANDARD)) {
    Serial.println("ERROR: MAX30105 not found. Check wiring.");
    while (1);
  }

  particleSensor.setup();
  particleSensor.setPulseAmplitudeRed(0xFF);
  particleSensor.setPulseAmplitudeGreen(0);

  Serial.println("Time (s), BPM, Avg BPM, Rapid Changes, Temp (°C), GSR Value, Piezo Value");
}

void loop() {
  long irValue = particleSensor.getIR();

  // Smooth LM35 Temperature Reading
  float tempSum = 0;
  for (int i = 0; i < 5; i++) {
    tempSum += analogRead(LM35_PIN) * (5.0 / 1023.0) * 11.0;
    delay(2);
  }
  float temperatureC = tempSum / 5.0;

  // Read GSR Sensor
  int gsrValue = analogRead(GSR_PIN);

  // Read Piezoelectric Sensor
  int piezoValue = analogRead(PIEZO_PIN);

  if (irValue < 50000) {
    Serial.println("No finger detected!");
    return;
  }

  if (checkForBeat(irValue)) {
    long delta = millis() - lastBeat;
    lastBeat = millis();
    beatsPerMinute = 60.0 / (delta / 1000.0);

    if (beatsPerMinute < 255 && beatsPerMinute > 20) {
      rates[rateSpot++] = (byte)beatsPerMinute;
      rateSpot %= RATE_SIZE;

      beatAvg = 0;
      for (byte i = 0; i < RATE_SIZE; i++)
        beatAvg += rates[i];
      beatAvg /= RATE_SIZE;

      if (abs(beatsPerMinute - stableBPM) >= 25) {
        stableCounter++;
        if (stableCounter >= 3) {
          rapidChanges++;
          stableBPM = beatsPerMinute;
          stableCounter = 0;
        }
      } else {
        stableCounter = 0;
      }

      prevBPM = beatsPerMinute;
    }
  }

  Serial.print(millis() / 1000.0); Serial.print(",");
  Serial.print(beatsPerMinute); Serial.print(",");
  Serial.print(beatAvg); Serial.print(",");
  Serial.print(rapidChanges); Serial.print(",");
  Serial.print(temperatureC); Serial.print(",");
  Serial.print(gsrValue / 102.4); Serial.print(","); // GSR %
  Serial.println(piezoValue /102.4); // Piezo value

  delay(10);
}
