/*
   Blink
   Turns on an LED on for one second, then off for one second, repeatedly.

   This example code is in the public domain.
   */
#include "bmp085.h"
#include <Wire.h>

#define LED 13

BMP085 PressureSensor = BMP085(3);


void setup() {                
	// initialize serial interface
	Serial.begin(9600);
	Serial.println("Initializing...");

	// initialize I2C interface
	Wire.begin();

	// initialize pressure sensor
	PressureSensor.begin();

	Serial.println("Initialization completed.");

	pinMode(LED, OUTPUT);
}

void loop() {
	Serial.print("Temperature: ");
	Serial.println(PressureSensor.readTemperature() / 10.0);
	Serial.print("Pressure: ");
	Serial.println(PressureSensor.readPressure());
	digitalWrite(LED, HIGH);   // set the LED on
	delay(100);              // wait for a second
	digitalWrite(LED, LOW);    // set the LED off
	delay(100);


	// wait for a second
}

// vim: ft=cpp
