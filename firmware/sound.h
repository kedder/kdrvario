#ifndef sound_h
#define sound_h

#include "vario.h"

class Sound {
	private:
		Vario *_vario;
		unsigned long _tonestart;
		bool _silent;

		int calc_pitch(int vspeed);
		int calc_duration(int vspeed);
	public:
		Sound(Vario *vario);
		void start();
		void stop();
		void update();
};

#endif
