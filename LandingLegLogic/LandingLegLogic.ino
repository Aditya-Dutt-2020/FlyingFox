#include <Servo.h>
#define echo 2
#define trig 3
#define THRESHDIST 50


Servo myservo;

long duration;
int distance;


void setup() {
  pinMode(echo, INPUT);
  pinMode(trig, OUTPUT);
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
}

void loop() {
  myservo.write(getDist() > THRESHDIST ? 0 : 180);
}


int getDist()
{
  digitalWrite(trig, LOW);
  delayMicroseconds(2);

  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);

  duration = pulseIn(echo, HIGH);
  distance = duration * 0.034 / 2;
  return distance;
}