#include "PinDefinitions.h"
#include "LandingLegLogic.h"
#include "GPSLogic.h"
#include "Communication.h"

void setup() {
  pinMode(BUILTIN_LED, OUTPUT);
  Serial.begin(115200);
  serial_connection.begin(9600);
  bigDisp.attach(bigDispPin);
  smallDisp.attach(smallDispPin);
  setup_wifi();
  client.setCallback(callback);
  while(!client.connected())
    reconnect();
}

void loop() {
  client.loop();
  int x;
//landingLogic();
  getLatLon();
  char GPSBuff[50];
  sprintf(GPSBuff, "%f %f", latlon[0], latlon[1]);
  //Serial.println(GPSBuff);
  client.publish("outTopic", GPSBuff);
  /*
  0.15 deg/us
  
  1200 = 180 deg
  go between 900 and 2100
  */
  bigDisp.writeMicroseconds(bigStat ? 900 : 2100);
  smallDisp.writeMicroseconds(smallStat ? 900 : 2100);

}

