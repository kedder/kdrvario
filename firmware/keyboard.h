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
#ifndef keyboard_h
#define keyboard_h


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
