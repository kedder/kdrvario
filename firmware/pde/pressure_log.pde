#include <Wire.h>

#include "bmp085.h"
#include "log.h"
#include "vario.h"

#define LED 13

BMP085 PressureSensor = BMP085(3);

int cnt = 0;

void setup() {                
	// initialize serial interface
	Serial.begin(57600);
	log("setup", "Initializing...");

	// initialize I2C interface
	Wire.begin();

	// initialize pressure sensor
	PressureSensor.begin();

	log("setup", "Initialization completed.");

	pinMode(LED, OUTPUT);
}

void loop() {

	if (cnt == 0) {
		log("temp", PressureSensor.readTemperature());
		cnt = 1;
	}
	log("pressure", PressureSensor.readPressure());
	cnt--;
	delay(30);
}

// vim: ft=cpp
