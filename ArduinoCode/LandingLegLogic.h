/*#include <Servo.h>
#include "PinDefinitions.h"
#define THRESHDIST 50
Servo landingServo;

long duration;
int distance;
int getDist();
void landingLogic();


void landingLogic()
{
  landingServo.write(getDist() > THRESHDIST ? 0 : 180);
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
}*/