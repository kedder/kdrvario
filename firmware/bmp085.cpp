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
/*
 * Support for Bosch BMP085 barometric pressure sensor
 */
#include <Wire.h>
#include <Arduino.h>

#include "bmp085.h"

#define BMP085_ADDRESS 0x77  // I2C address of BMP085
/*
 * Public members
 */
BMP085::BMP085(int8_t mode) {
	_mode = mode;
}

void BMP085::begin() {
	ac1 = readInt(0xAA);
	ac2 = readInt(0xAC);
	ac3 = readInt(0xAE);
	ac4 = readInt(0xB0);
	ac5 = readInt(0xB2);
	ac6 = readInt(0xB4);
	b1 = readInt(0xB6);
	b2 = readInt(0xB8);
	mb = readInt(0xBA);
	mc = readInt(0xBC);
	md = readInt(0xBE);
}

long BMP085::readTemperature() {
	return compensateTemperature(readUncompensatedTemperature());
}

long BMP085::readPressure() {
	return compensatePressure(readUncompensatedPressure());
}

/*
 * Private members
 */

long BMP085::compensateTemperature(unsigned int ut) {
	long x1, x2;

	x1 = (((long)ut - (long)ac6)*(long)ac5) >> 15;
	x2 = ((long)mc << 11)/(x1 + md);
	b5 = x1 + x2;

	return ((b5 + 8)>>4);  
}

unsigned int BMP085::readUncompensatedTemperature() {
	unsigned int ut;

	// Write 0x2E into Register 0xF4
	// This requests a temperature reading
	Wire.beginTransmission(BMP085_ADDRESS);
	Wire.write(0xF4);
	Wire.write(0x2E);
	Wire.endTransmission();

	// Wait at least 4.5ms
	delay(5);

	// Read two bytes from registers 0xF6 and 0xF7
	ut = readInt(0xF6);
	return ut;
}

long BMP085::compensatePressure(unsigned long up) {
	long x1, x2, x3, b3, b6, p;
	unsigned long b4, b7;

	b6 = b5 - 4000;
	// Calculate B3
	x1 = (b2 * (b6 * b6)>>12)>>11;
	x2 = (ac2 * b6)>>11;
	x3 = x1 + x2;
	b3 = (((((long)ac1)*4 + x3)<<_mode) + 2)>>2;

	// Calculate B4
	x1 = (ac3 * b6)>>13;
	x2 = (b1 * ((b6 * b6)>>12))>>16;
	x3 = ((x1 + x2) + 2)>>2;
	b4 = (ac4 * (unsigned long)(x3 + 32768))>>15;

	b7 = ((unsigned long)(up - b3) * (50000>>_mode));
	if (b7 < 0x80000000)
		p = (b7<<1)/b4;
	else
		p = (b7/b4)<<1;

	x1 = (p>>8) * (p>>8);
	x1 = (x1 * 3038)>>16;
	x2 = (-7357 * p)>>16;
	p += (x1 + x2 + 3791)>>4;

	return p;
}

unsigned long BMP085::readUncompensatedPressure() {
	unsigned char msb, lsb, xlsb;
	unsigned long up = 0;

	// Write 0x34+(_mode<<6) into register 0xF4
	// Request a pressure reading w/ oversampling setting
	Wire.beginTransmission(BMP085_ADDRESS);
	Wire.write(0xF4);
	Wire.write(0x34 + (_mode<<6));
	Wire.endTransmission();

	// Wait for conversion, delay time dependent on _mode
	delay(2 + (3<<_mode));

	// Read register 0xF6 (MSB), 0xF7 (LSB), and 0xF8 (XLSB)
	Wire.beginTransmission(BMP085_ADDRESS);
	Wire.write(0xF6);
	Wire.endTransmission();
	Wire.requestFrom(BMP085_ADDRESS, 3);

	// Wait for data to become available
	while(Wire.available() < 3)
		;
	msb = Wire.read();
	lsb = Wire.read();
	xlsb = Wire.read();

	up = (((unsigned long) msb << 16) | ((unsigned long) lsb << 8) | (unsigned long) xlsb) >> (8-_mode);

	return up;
}


int BMP085::readInt(unsigned char address) {
	// Read 2 bytes from the BMP085
	// First byte will be from 'address'
	// Second byte will be from 'address'+1
	unsigned char msb, lsb;

	Wire.beginTransmission(BMP085_ADDRESS);
	Wire.write(address);
	Wire.endTransmission();

	Wire.requestFrom(BMP085_ADDRESS, 2);
	while(Wire.available()<2) {
	}
	msb = Wire.read();
	lsb = Wire.read();

	return (int) msb<<8 | lsb;
}
