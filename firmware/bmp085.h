/*
 * Support for Bosch BMP085 barometric pressure sensor
 */
#ifndef BMP085_h
#define BMP085_h

class BMP085 {
	private:
		int _mode;
		
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
		BMP085(int mode);
		void begin();
		long readTemperature();
		long readPressure();
};

#endif
