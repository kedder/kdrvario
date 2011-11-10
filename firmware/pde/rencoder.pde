#include <LiquidCrystal.h>
#include <avr/pgmspace.h>

#include "keyboard.h"

#define RE_A 2
#define RE_B 3
#define BUTTON 10
#define LED 13


LiquidCrystal l(7, 6, 5, 4, 9, 8);
volatile int counter = 0;
int buttoncnt = 0;

void setup() {                
	// initialize serial interface
	Serial.begin(57600);

	l.begin(16, 2);
	l.print("KDR Vario");

	pinMode(LED, OUTPUT);
	keyboard.begin();
}

void processKeyboard() {
	uint8_t btn;
    while (btn = keyboard.read()) {
		switch (btn) {
			case BUTTON_RIGHT:
				counter++;
				break;
			case BUTTON_LEFT:
				counter--;
				break;
			case BUTTON_OK:
				buttoncnt++;
		}
	}
}

void loop() {
	keyboard.poll();

	processKeyboard();

	l.setCursor(0, 1);
	l.print(counter);
	l.print(" ");
	l.setCursor(10, 1);
	l.print(buttoncnt);

	// simulate slow processing
	delay(50);
}



// vim: ft=cpp
