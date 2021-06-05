#define LPWM_PIN 9
#define LCONTROL_PIN 8
#define RCONTROL_PIN 7
#define RPWM_PIN 6

void setup(){
	pinMode(LED_BUILTIN, OUTPUT);
}

void loop(){
	digitalWrite(LED_BUILTIN, HIGH);
	delay(500);
	digitalWrite(LED_BUILTIN, LOW);
	delay(500);
}
