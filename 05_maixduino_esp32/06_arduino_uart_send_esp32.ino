// Copyright (c) 2019 aNoken
// Arduino IDE compile code
//arduino-esp ver 1.04

#include <Arduino.h>
HardwareSerial serial_ext(2);

void setup() {
  Serial.begin(115200);
  serial_ext.begin(115200, SERIAL_8N1, 1, 3);
}

void loop() {
  if ( serial_ext.available() > 0 ) {
    String str = serial_ext.readStringUntil('\n');
    int data = str.toInt();
    Serial.print("data:");
    Serial.println(data);
  }
  vTaskDelay(10 / portTICK_RATE_MS);
}
