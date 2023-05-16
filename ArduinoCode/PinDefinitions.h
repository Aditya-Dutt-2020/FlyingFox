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

bool bigStat = false;
bool smallStat = false;
#endif