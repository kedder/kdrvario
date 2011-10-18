#include "log.h"
#include "vario.h"
#include "sound.h"

Vario vario = Vario();
Sound sound = Sound(&vario);

void setup() {                
	// initialize serial interface
	Serial.begin(57600);
	log("setup", "Initializing...");
	log("setup", "Initialized");
}

void loop() {
	sound.update();
}

// vim: ft=cpp
