#include <WProgram.h>
#include "filter.h"

AlphaBetaFilter::AlphaBetaFilter(float alpha, float beta) {
	_alpha = alpha;
	_beta = beta;

	_lastts = 0;
	_position = 0;
	_velocity = 0;
	_initialized = false;
}

void AlphaBetaFilter::filter(long value) {
	unsigned long now = millis();
	if (!_initialized) {
		// State is not initialized yet. Use first value to calibrate
		// position.
		_position = value;
		_lastts = now;
		_initialized = true;
		return;
	}

	float dt = (now - _lastts) / 1000.0;
    _lastts = now;

	float a = _alpha * dt;
	float b = _beta * dt * dt;

	long pos = _position + _velocity * dt;
	int vel = _velocity;

	long r = value - pos;

	pos += a * r;
	vel += b * r/dt;

	_position = pos;
	_velocity = vel;
}

long AlphaBetaFilter::getPosition() {
	return _position;
}
int AlphaBetaFilter::getVelocity() {
	return _velocity;
}

