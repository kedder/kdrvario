/*
   Blink
   Turns on an LED on for one second, then off for one second, repeatedly.

   This example code is in the public domain.
   */
#include <Wire.h>

#include "bmp085.h"
#include "log.h"

#define LED 13

BMP085 PressureSensor = BMP085(3);


void setup() {                
	// initialize serial interface
	Serial.begin(9600);
	log("setup", "Initializing...");

	// initialize I2C interface
	Wire.begin();

	// initialize pressure sensor
	PressureSensor.begin();

	log("setup", "Initialization completed.");

	pinMode(LED, OUTPUT);
}

void loop() {
	log("temp", PressureSensor.readTemperature() / 10.0);
	log("pressure", PressureSensor.readPressure());
	digitalWrite(LED, HIGH);   // set the LED on
	delay(50);              // wait for a second
	digitalWrite(LED, LOW);    // set the LED off
	delay(50);


	// wait for a second
}

// vim: ft=cpp
