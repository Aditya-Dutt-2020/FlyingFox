#include <TinyGPSPlus.h>
#include <SoftwareSerial.h>
#include "PinDefinitions.h"

SoftwareSerial serial_connection(gpsRX, gpsTX);

TinyGPSPlus gps;
void getLatLon();
double latlon[2];
void getLatLon()
{
  while (serial_connection.available() > 0)
    if (gps.encode(serial_connection.read()) && gps.location.isValid())
    {
      if (gps.location.lat() >= 30 && gps.location.lng() <= -20)
      latlon[0] = gps.location.lat();
      latlon[1] = gps.location.lng();
    }
}


