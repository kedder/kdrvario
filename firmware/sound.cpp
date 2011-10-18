#include <WProgram.h>

#include "vario.h"
#include "sound.h"
//#include "wiring.h"


#define SOUND_PIN 11

Sound::Sound(Vario *vario) {
	_vario = vario;
	_silent = false;
	_tonestart = 0;
}

int Sound::calc_pitch(int vspeed) {
	return 440;
}

int Sound::calc_duration(int vspeed) {
	return 100;
}

void Sound::start() {
}

void Sound::stop() {
}

void Sound::update() {
	int vspeed = _vario->get_vertical_speed();
	int pitch = calc_pitch(vspeed);
    int duration = calc_duration(vspeed);

	unsigned long now = millis();
	if (vspeed > 0) {
		if (_tonestart + duration < now) {
			_silent = !_silent;
			_tonestart = now;
		}
	}
	else {
		_silent = false;
	}

	if (_silent) {
		// sound off
		noTone(SOUND_PIN);
	}
	else {
		// set sound pitch
		tone(SOUND_PIN, pitch);
	}
}
