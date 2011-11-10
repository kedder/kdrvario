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
#include <math.h>
#include "atmosphere.h"

#define STDPRESSURE 101325

Atmosphere::Atmosphere() {
	_zeropressure = STDPRESSURE;
}

long Atmosphere::pressureToAlt(long pressure) {
	float pr = (float)pressure / (float)_zeropressure;
	//return 44330 * (1 - pow(pr, 1/5.255));
	return 44330.0 * (1 - pow(pr, 1/5.255)) * 100;
}

long Atmosphere::getZeroPressure() {
	return _zeropressure;
}

void Atmosphere::setZeroPressure(long zeropressure) {
	_zeropressure = zeropressure;
}
