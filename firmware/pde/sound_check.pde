#include "log.h"
#include "vario.h"
#include "sound.h"

Vario vario = Vario();
Sound sound = Sound(&vario);
int add = -1;

char buf[32];
void control() {
	if (!Serial.available()) {
		return;
	}
	// read line
	char *ptr = buf;
	for (short cnt = 0; cnt < sizeof(buf) - 1; cnt++) {
		while (!Serial.available()) {} // wait for next available byte
		char c = Serial.read();
		if (c == -1 || c == '\n') {
			buf[cnt] = 0;
			break;
		}
        buf[cnt] = c;
	}

	//log("buf", buf);
	int value = atoi(buf);
	//log("read", value);
	sound.start();
	vario.set_vertical_speed(value);
	add = 0;
}

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
	control();
	//delay(4);
}



// vim: ft=cpp
