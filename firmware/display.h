#ifndef display_h
#define display_h

class Display {
	private:
		long lastalt;
	public:
		void begin();
		void showAlititude(long altitude);
		void showVSpeed(int vspeed);
		void showPressure(long pressure);
		void showTemperature(long temp);
};

#endif
