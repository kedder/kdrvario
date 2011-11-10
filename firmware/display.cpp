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
#include <LiquidCrystal.h>
#include "display.h"

LiquidCrystal lcd(7, 6, 5, 4, 9, 8);

void Display::begin() {
	lcd.begin(16, 2);
	lcd.print("KDR Vario");
}

void Display::showAlititude(long altitude) {
    long diff = abs(lastalt - altitude);
	if (diff < 50) {
		// do not update altitude if it has not changed significantly to void
		// flickering
		return;
	}
	lastalt = altitude;

	lcd.setCursor(0, 0);
	lcd.print("A:      ");
	lcd.setCursor(3, 0);
	lcd.print(altitude / 100);
}
void Display::showVSpeed(int vspeed) {
	lcd.setCursor(8, 0);
	lcd.print("V:      ");
	float vs = vspeed / 10 / 10.0;
	lcd.setCursor(vs < 0 ? 11 : 12, 0);
	lcd.print(vs);
}

void Display::showTemperature(long temp) {
	lcd.setCursor(0, 1);
	lcd.print("T:              ");
	lcd.setCursor(3, 1);
	lcd.print((float)temp / 10);
}
