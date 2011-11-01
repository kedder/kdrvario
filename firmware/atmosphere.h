#ifndef atmosphere_h
#define atmosphere_h

class Atmosphere {
	private:
		long _zeropressure;

	public:
		Atmosphere();
		long pressureToAlt(long pressure);
		long getZeroPressure();
		void setZeroPressure(long zeropressure);
};

#endif
