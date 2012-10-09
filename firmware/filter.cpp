/* 
  KDR Vario. Digital variometer based on Arduino.
  Copyright (C) 2011 Andrey Lebedev

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
#include <Arduino.h>
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

	float pos = _position + _velocity * dt;
	float vel = _velocity;

	float r = value - pos;

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

