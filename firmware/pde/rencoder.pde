#include <LiquidCrystal.h>
#include <avr/pgmspace.h>

#define RE_A 2
#define RE_B 3
#define LED 13

LiquidCrystal l(7, 6, 5, 4, 9, 8);
volatile int counter = 0;

void reChange() {
	static uint8_t old_AB = 3;  //lookup table index
	static int8_t encval = 0;   //encoder value
	static const int8_t enc_states [] PROGMEM = 
		{0,-1,1,0,1,0,0,-1,-1,0,0,1,0,1,-1,0};  //encoder lookup table

    old_AB <<=2;  //remember previous state
	bitWrite(old_AB, 1, digitalRead(RE_A));
	bitWrite(old_AB, 0, digitalRead(RE_B));

	int8_t state = pgm_read_byte(&(enc_states[( old_AB & 0x0f )]));
	//Serial.print("state ");
	//Serial.print(( old_AB & 0x0f ));
	//Serial.print(" ");
	//Serial.println(state);
	encval += state;
	if( encval > 1 ) {  //two steps forward
		counter++;
		encval = 0;
	}
	else if( encval < -1 ) {  //two steps backwards
		counter--;
		encval = 0;
	}

	// blink the led
	static bool ledstate = LOW;
	ledstate = !ledstate;
	digitalWrite(LED, ledstate);
}

void setup() {                
	// initialize serial interface
	Serial.begin(57600);

	l.begin(16, 2);
	l.print("KDR Vario");

	// configure pins
	pinMode(RE_A, INPUT);
	pinMode(RE_B, INPUT);
	pinMode(LED, OUTPUT);
    
	// enable internal pullups
	digitalWrite(RE_A, HIGH`);
	digitalWrite(RE_B, HIGH);

	attachInterrupt(1, reChange, CHANGE);
	attachInterrupt(0, reChange, CHANGE);
}

void loop() {
	l.setCursor(0, 1);
	l.print(counter);
	l.print("   ");
}

// vim: ft=cpp
