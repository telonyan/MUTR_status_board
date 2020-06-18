int a_pin0 = A0;
int a_pin1 = A1;
int a_pin2 = A2;
int a_pin3 = A3;
int a_pin4 = A4;
int a_pin5 = A5;

int d_pin1 = 1;
int d_pin2 = 2;
int d_pin3 = 3;
int d_pin4 = 4;
int d_pin5 = 5;
int d_pin6 = 6;
int d_pin7 = 7;
int d_pin8 = 8;
int d_pin9 = 9;
int d_pin10 = 10;
int d_pin11 = 11;
int d_pin12 = 12;
int d_pin13 = 13;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(analogRead(a_pin0));
  Serial.println(analogRead(a_pin1));
  Serial.println(analogRead(a_pin2));
  Serial.println(analogRead(a_pin3));
  Serial.println(analogRead(a_pin4));
  Serial.println(analogRead(a_pin5));
  Serial.println(digitalRead(d_pin1));
  Serial.println(digitalRead(d_pin2));
  Serial.println(digitalRead(d_pin3));
  Serial.println(digitalRead(d_pin4));
  Serial.println(digitalRead(d_pin5));
  Serial.println(digitalRead(d_pin6));
  Serial.println(digitalRead(d_pin7));
  Serial.println(digitalRead(d_pin8));
  Serial.println(digitalRead(d_pin9));
  Serial.println(digitalRead(d_pin10));
  Serial.println(digitalRead(d_pin11));
  Serial.println(digitalRead(d_pin12));
  Serial.println(digitalRead(d_pin13));
  delay(1000);
}
