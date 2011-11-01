#include <Wire.h>

#include "bmp085.h"
#include "log.h"
#include "vario.h"
#include "filter.h"
#include "atmosphere.h"

#define LED 13

BMP085 pressureSensor(3);
AlphaBetaFilter filter(1.2923, 0.86411);
Atmosphere atmosphere = Atmosphere();

int cnt = 0;

void setup() {                
	// initialize serial interface
	Serial.begin(57600);
	log("setup", "Initializing...");

	// initialize I2C interface
	Wire.begin();

	// initialize pressure sensor
	pressureSensor.begin();

	log("setup", "Initialization completed.");

	pinMode(LED, OUTPUT);
}

void loop() {

	if (cnt == 0) {
		log("temp", pressureSensor.readTemperature());
		cnt = 4;
	}
	long pressure = pressureSensor.readPressure();
	log("pressure", pressure);
	cnt--;

	long altitude = atmosphere.pressureToAlt(pressure);
	log("altitude", altitude);
	filter.filter(altitude);

	log("filtered", filter.getPosition());
	log("velocity", filter.getVelocity());
	
	delay(50);
}

// vim: ft=cpp
