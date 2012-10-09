/* 
  KDR Vario. Digital variometer based on Arduino.
  Copyright (C) 2011 Andrey Lebedev

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
#include <Arduino.h>
#include <Wire.h>

#include "bmp085.h"
#include "log.h"
#include "filter.h"
#include "atmosphere.h"
#include "sound.h"
#include "display.h"
#include "keyboard.h"


BMP085 pressureSensor(0);
//AlphaBetaFilter filter(1.2923, 0.86411);
//welf.
AlphaBetaFilter filter(1.0, 1.0);
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
	sound.start();
	keyboard.begin();

	log("setup", "Initialization completed.");

}

void loop() {
	if (cnt == 0) {
		long temp = pressureSensor.readTemperature();
		display.showTemperature(temp);
		log("temp", temp);
		//cnt = 1000;
		cnt = 1;
	}
	cnt--;

	long pressure = pressureSensor.readPressure();

	long altitude = atmosphere.pressureToAlt(pressure);
	filter.filter(altitude);

	int velocity = filter.getVelocity();

	sound.update(velocity);

	display.showAlititude(filter.getPosition());
	display.showVSpeed(velocity);

	keyboard.poll();
	uint8_t key = keyboard.read();
	if (key) {
		log("key", key);
	}
	
	//log("pressure", pressure);
	log("altitude", altitude);
	log("filtered", filter.getPosition());
	log("velocity", velocity);
	//delay(10);
}

// vim: ft=cpp
