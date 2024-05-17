#include <WiFi.h>
#include <ESP32Servo.h>

#define SERVO 13

// Update these with values suitable for your network.
const char* ssid = "CuongLM";
const char* password = "lamgicomatkhau";

WiFiServer server(80);

Servo myServo;
int currentAngle = 0; // Biến lưu trữ góc hiện tại của servo

void setup() {
  Serial.begin(115200);

  myServo.attach(SERVO);

  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("Connected to WiFi");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  server.begin();
}

void loop() {
  WiFiClient client = server.available();

  if (client) {
    while (client.connected()) {
      if (client.available()) {
        String command = client.readStringUntil('\n');
        Serial.println("Command: " + command);
        command.trim();
        int newAngle = command.toInt();
        if (newAngle >= 0 && newAngle <= 180) { // Kiểm tra góc mới có hợp lệ không
          currentAngle = newAngle; // Cập nhật góc hiện tại
          myServo.write(currentAngle); // Di chuyển servo đến góc mới
        }
        delay(1);
      } else {
        myServo.write(currentAngle); // Giữ servo ở góc hiện tại
      }
    }
    client.stop();
    Serial.println("Client disconnected");
  } else {
    myServo.write(currentAngle); // Giữ servo ở góc hiện tại
  }
}
