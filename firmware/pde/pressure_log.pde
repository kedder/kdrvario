#include <Wire.h>

#include "bmp085.h"
#include "log.h"
#include "filter.h"
#include "atmosphere.h"
#include "sound.h"
#include "display.h"


BMP085 pressureSensor(3);
//AlphaBetaFilter filter(1.2923, 0.86411);
//welf.
AlphaBetaFilter filter(1.7, 1.7);
Atmosphere atmosphere = Atmosphere();
Sound sound = Sound();
Display display = Display();


int cnt = 0;

void setup() {                
	// initialize serial interface
	Serial.begin(57600);
	log("setup", "Initializing...");

	display.begin();

	// initialize I2C interface
	Wire.begin();

	// initialize pressure sensor
	pressureSensor.begin();

	log("setup", "Initialization completed.");

	sound.start();
}

void loop() {
	if (cnt == 0) {
		long temp = pressureSensor.readTemperature();
		display.showTemperature(temp);
		log("temp", temp);
		cnt = 2000;
	}
	cnt--;

	long pressure = pressureSensor.readPressure();

	long altitude = atmosphere.pressureToAlt(pressure);
	filter.filter(altitude);

	int velocity = filter.getVelocity();

	sound.update(velocity);

	display.showAlititude(filter.getPosition());
	display.showVSpeed(velocity);
	
	//log("pressure", pressure);
	log("altitude", altitude);
	log("filtered", filter.getPosition());
	log("velocity", velocity);
	//delay(10);
}

// vim: ft=cpp
