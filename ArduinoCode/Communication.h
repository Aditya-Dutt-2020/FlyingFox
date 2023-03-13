#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include "PinDefinitions.h"
const char* ssid = "ANRV_WIFI";
const char* password = "flyingfox";
const char* mqtt_server = "fe80::bccf:7a85:6bd6:88c4";
const char* mqtt_username = "ANRV_Mos";
const char* mqtt_password = "flyingMos";
const char* clientID = "Dutts ESP";
WiFiClient wifiClient;
PubSubClient client(mqtt_server, 1883, wifiClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE	(50)
char msg[MSG_BUFFER_SIZE];
int value = 0;

void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  //WiFi.mode(WIFI_STA);
  IPAddress ip(192, 168, 1, 100);
  IPAddress gateway(192, 168, 1, 1);
  IPAddress subnet(255, 255, 255, 0);
  WiFi.config(ip, gateway, subnet);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(WiFi.status());
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
    
  }
  Serial.println();

  if ((char)payload[0] == 'B')
  {
    digitalWrite(BUILTIN_LED, LOW);
    Serial.println("spinning big");
    bigDisp.write(180);
    SPINNING = true;
    startTime = millis();
  }
  if ((char)payload[0] == 'S')
  {
    digitalWrite(BUILTIN_LED, LOW);
    Serial.println("spinning small");
    smallDisp.write(180);
    SPINNING = true;
    startTime = millis();
  }
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    // Attempt to connect
    if (client.connect(clientID, mqtt_username, mqtt_password)) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("outTopic", "hello world");
      // ... and resubscribe
      client.subscribe("inTopic");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 1 seconds");
      // Wait 5 seconds before retrying
      delay(1000);
    }
  }
}