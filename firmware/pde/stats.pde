#include <Wire.h>
#include <math.h>

#include "bmp085.h"
#include "log.h"
#include "vario.h"


#define BUFSIZE 10

BMP085 PressureSensor = BMP085(0);

long readings[BUFSIZE];

long average();
float stdev(long mean);

void setup() {                
	// initialize serial interface
	Serial.begin(57600);
	log("setup", "Initializing...");

	// initialize I2C interface
	Wire.begin();

	// initialize pressure sensor
	PressureSensor.begin();

	log("setup", "Initialization completed.");
}

void loop() {

	log("temp", PressureSensor.readTemperature());

	unsigned long start = millis();
	for (int i = 0; i < BUFSIZE; i++) {
		readings[i] = PressureSensor.readPressure();
		//delay(100);
	}
	unsigned long end = millis();

	// calculate stats
	log("rate", BUFSIZE * (100000 / (end - start)) / 100);

	long avg = average();
	log("pressure", avg);
	float rms = stdev(avg);
	log("stdev", rms);
}

long average() {
	long sum = 0;
    for (int i = 0; i < BUFSIZE; i++) {
		sum += readings[i];
	}

	return sum / BUFSIZE;
}

float stdev(long mean) {
	long sum = 0;
    for (int i = 0; i < BUFSIZE; i++) {
		int value = readings[i] - mean;
		sum += value * value;
	}
	return sqrt(sum / BUFSIZE);
}

// vim: ft=cpp
