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
#ifndef BMP085_h
#define BMP085_h

class BMP085 {
	private:
		int8_t _mode;
		
		// Calibration values
		int ac1;
		int ac2; 
		int ac3; 
		unsigned int ac4;
		unsigned int ac5;
		unsigned int ac6;
		int b1; 
		int b2;
		int mb;
		int mc;
		int md;

		// b5 is calculated in readTemperature(...), this variable is also
		// used in readPressure(...) so readTemperature(...) must be called
		// before readPressure(...).
		long b5; 

		int readInt(unsigned char address);
		unsigned int readUncompensatedTemperature();
		unsigned long readUncompensatedPressure();
		long compensateTemperature(unsigned int ut);
		long compensatePressure(unsigned long up);

	public:
		BMP085(int8_t mode);
		void begin();
		long readTemperature();
		long readPressure();
};

#endif
