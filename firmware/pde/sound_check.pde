#include "log.h"
#include "vario.h"
#include "sound.h"

Vario vario = Vario();
Sound sound = Sound(&vario);
int add = -1;

void setup() {                
	// initialize serial interface
	Serial.begin(57600);
	log("setup", "Initializing...");
	log("setup", "Initialized");
	vario.set_vertical_speed(20);
}

void loop() {
	sound.update();
	if (vario.get_vertical_speed() < -500) {
		add = 1;
	}
	if (vario.get_vertical_speed() > 500) {
		add = -1;
	}
	vario.set_vertical_speed(vario.get_vertical_speed() + add);
	//delay(1);
}

// vim: ft=cpp
