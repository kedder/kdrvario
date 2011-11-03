#include <LiquidCrystal.h>
#include "display.h"

LiquidCrystal lcd(7, 6, 5, 4, 3, 2);

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
