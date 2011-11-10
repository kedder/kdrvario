#ifndef keyboard_h
#define keyboard_h

#include "wiring.h"

#define KEYBOARD_BUFFER_SIZE 16

// Buttons

#define BUTTON_LEFT 1
#define BUTTON_RIGHT 2
#define BUTTON_OK 3

class Keyboard {
	private:
		uint8_t _buf[KEYBOARD_BUFFER_SIZE];
		int8_t _ptr;

	public:
		Keyboard();
		void begin();
		void poll();
		uint8_t read();
		void push(uint8_t button);
};

extern Keyboard keyboard;

#endif
