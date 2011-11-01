#ifndef sound_h
#define sound_h

class Sound {
	private:
		unsigned long _tonestart;
		bool _silent;
		bool _enabled;

		int calc_pitch(int vspeed);
		int calc_duration(int vspeed);
	public:
		Sound();
		void start();
		void stop();
		void update(int vspeed);
};

#endif
