#include <WProgram.h>

#include "vario.h"
#include "sound.h"
#include "log.h"
//#include "wiring.h"


#define SOUND_PIN 11

#define MIN_DURATION 30
#define MAX_DURATION 300
#define INF_DURATION -1

// Maximum vertical speed supported (in cm/s)
#define MAX_VSPEED 500

Sound::Sound(Vario *vario) {
	_vario = vario;
	_silent = false;
	_tonestart = 0;
}

int Sound::calc_pitch(int vspeed) {
	log("vspeed", vspeed);
	unsigned long pitch;
	if (vspeed > MAX_VSPEED) {
		vspeed = MAX_VSPEED;
	}
	if (vspeed < -MAX_VSPEED) {
		vspeed = -MAX_VSPEED;
	}
	vspeed = vspeed + MAX_VSPEED;
	pitch = ((long) vspeed * (long) vspeed * (long)vspeed);
	log("cubed", pitch);
	pitch = pitch >> 19; 
	pitch += 80;
	log("pitch", pitch);
	return pitch;
}

int Sound::calc_duration(int vspeed) {
	if (vspeed <= 0) {
		return INF_DURATION;
	}
	if (vspeed > MAX_VSPEED) {
		vspeed = MAX_VSPEED;
	}
	int duration = map(vspeed, 0, MAX_VSPEED, MAX_DURATION, MIN_DURATION);
	//log("duration", duration);
	return duration;
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
