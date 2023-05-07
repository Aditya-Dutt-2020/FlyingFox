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
  while(!client.connected()) {
    reconnect();
  }
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
  if (millis() >= startTime+dispSpinTime && SPINNING)
  {
    Serial.println("stopped spinning");
    bigDisp.write(90);
    smallDisp.write(90);
    SPINNING = false;
  }
}

