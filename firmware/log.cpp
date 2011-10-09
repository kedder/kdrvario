#include "WProgram.h"

void log(const char *key, double value) {
    Serial.print(key);
	Serial.print(':');
	Serial.println(value);
}
void log(const char *key, long value) {
    Serial.print(key);
	Serial.print(':');
	Serial.println(value);
}

void log(const char *key, int value) {
    Serial.print(key);
	Serial.print(':');
	Serial.println(value);
}

void log(const char *key, char *value) {
    Serial.print(key);
	Serial.print(':');
	Serial.println(value);
}

