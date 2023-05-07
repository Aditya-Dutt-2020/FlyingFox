#ifndef PINDEFS
#define PINDEFS
#include <Servo.h>

//#define echo A0
//#define trig A1
#define gpsRX 14
#define gpsTX 12
#define smallDispPin 5
#define bigDispPin 16
Servo smallDisp;
Servo bigDisp;

int dispSpinTime = 275;
bool SPINNING = false;
unsigned long startTime = 0;
#endif