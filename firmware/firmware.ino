#define LPWM_PIN 9
#define LCONTROL_PIN 8
#define RCONTROL_PIN 7
#define RPWM_PIN 6

int lSpeed = 0;
int rSpeed = 0;

void setup(){
	Serial.begin(115200);
	pinMode(LED_BUILTIN, OUTPUT);
}

void setMotorSpeeds(){
	// Make sure the speeds are within the acceptable range
	if(lSpeed < -255) lSpeed = -255;
	if(lSpeed > 255) lSpeed = 255;
	if(rSpeed < -255) rSpeed = -255;
	if(rSpeed > 255) rSpeed = 255;

	if(lSpeed < 0){
		digitalWrite(LCONTROL_PIN, HIGH);
		analogWrite(LPWM_PIN, 255+lSpeed);
	}else{
		digitalWrite(LCONTROL_PIN, LOW);
		analogWrite(LPWM_PIN, lSpeed);
	}

	if(rSpeed < 0){
		digitalWrite(RCONTROL_PIN, HIGH);
		analogWrite(RPWM_PIN, 255+rSpeed);
	}else{
		digitalWrite(RCONTROL_PIN, LOW);
		analogWrite(RPWM_PIN, rSpeed);
	}
}

void serialEvent(){
	char ident_char = (char)Serial.read();
	switch(ident_char){
		case 'm':
			lSpeed = Serial.parseInt();
			rSpeed = Serial.parseInt();
			Serial.read();
			setMotorSpeeds();
			break;
	}
}

void loop(){
	;
}
