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
