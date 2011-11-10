#include <avr/pgmspace.h>
#include "keyboard.h"

#define RE_A 2
#define RE_B 3
#define BUTTON 10

void ISR_rotaryEncoder();

Keyboard::Keyboard() {
	// clear buffer
	for (uint8_t i=0; i<KEYBOARD_BUFFER_SIZE; i++) {
		_buf[i] = 0;
	}
	_ptr = 0;
}

void Keyboard::begin() {
	// configure pins
	pinMode(RE_A, INPUT);
	pinMode(RE_B, INPUT);
	pinMode(BUTTON, INPUT);
    
	// enable internal pullups
	digitalWrite(RE_A, HIGH);
	digitalWrite(RE_B, HIGH);
	digitalWrite(BUTTON, HIGH);

	attachInterrupt(1, ISR_rotaryEncoder, CHANGE);
	attachInterrupt(0, ISR_rotaryEncoder, CHANGE);
}

void Keyboard::poll() {
	// read single button
	static bool laststate = HIGH;
	bool currstate = digitalRead(BUTTON);
	if (laststate != currstate) {
		laststate = currstate;
		if (currstate == LOW) {
			push(BUTTON_OK);
		}
	}
}

uint8_t Keyboard::read() {
	if (_ptr == -1) {
		return 0;
		// nothing in buffer
	}
	return _buf[_ptr--];
}

void Keyboard::push(uint8_t button) {
	if (_ptr+1 == KEYBOARD_BUFFER_SIZE) {
		// buffer overflow. ignore event.
		return;
	}
	_buf[++_ptr] = button;
}

void ISR_rotaryEncoder() {
	static uint8_t old_AB = 3;  //lookup table index
	static int8_t encval = 0;   //encoder value
	static const int8_t enc_states [] PROGMEM = 
		{0,-1,1,0,1,0,0,-1,-1,0,0,1,0,1,-1,0};  //encoder lookup table

    old_AB <<=2;  //remember previous state
	bitWrite(old_AB, 1, digitalRead(RE_A));
	bitWrite(old_AB, 0, digitalRead(RE_B));

	int8_t state = pgm_read_byte(&(enc_states[( old_AB & 0x0f )]));
	encval += state;
	if( encval > 1 ) {  //two steps forward
		keyboard.push(BUTTON_RIGHT);
		encval = 0;
	}
	else if( encval < -1 ) {  //two steps backwards
		keyboard.push(BUTTON_LEFT);
		encval = 0;
	}
}

Keyboard keyboard;
