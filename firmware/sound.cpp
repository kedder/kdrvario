#include <WProgram.h>

#include "sound.h"
#include "log.h"
//#include "wiring.h"


#define SOUND_PIN 11

#define MIN_DURATION 30
#define MAX_DURATION 200
#define INF_DURATION -1

// Maximum vertical speed supported (in cm/s)
#define MAX_VSPEED 500

#define MIN_PITCH 20
#define ZERO_PITCH 220
#define MAX_PITCH 1500
#define SILENT_LOW -18
#define SILENT_HIGH 18

Sound::Sound() {
	_silent = false;
	_tonestart = 0;
	_enabled = false;
}

int Sound::calc_pitch(int vspeed) {
	if (vspeed <=0) {               
		return map(vspeed, -MAX_VSPEED, 0, MIN_PITCH, ZERO_PITCH);
	}
	else {
		return map(vspeed, 0, MAX_VSPEED, ZERO_PITCH, MAX_PITCH);
	}
	/*
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
	*/
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
	_enabled = true;
}

void Sound::stop() {
	_enabled = false;
	noTone(SOUND_PIN);
}

void Sound::update(int vspeed) {
	if (!_enabled) {
		return;
	}

	if (vspeed >= SILENT_LOW && vspeed <= SILENT_HIGH) {
		noTone(SOUND_PIN);
		return;
	}

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
