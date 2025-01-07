#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* ssid = "vivo T1";     // Replace with your Wi-Fi SSID
const char* password = "haarit1905"; // Replace with your Wi-Fi password

ESP8266WebServer server(80);

// Dummy moisture sensor value (replace with actual sensor reading logic)
int moistureValue = 0;

void setup() {
  Serial.begin(115200);
  delay(100);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // Define server routes
  server.on("/", HTTP_GET, handleRoot);

  // Start server
  server.begin();
  Serial.println("Server started");
}

void loop() {
  server.handleClient();
  int moistureValue = analogRead(A0);
  String webpage = "<html><head><title>Moisture Sensor Data</title></head><body>";
  webpage += "<h1>Moisture Sensor Data</h1>";
  webpage += "<p>Moisture Value: " + String(moistureValue) + "</p>";
  webpage += "</body></html>";

  // Send response to client
  server.send(200, "text/html", webpage);
  delay(2000);
}

void handleRoot() {
  // Construct HTML response
  
}
