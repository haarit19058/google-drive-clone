#include <Servo.h>

Servo myservo;  // create servo object to control a servo
int pos = 0;    // variable to store the servo position

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
   // Rotate servo from 0 to 180 degrees
  

  myservo.write(180);
  delay(600);
  myservo.detach();
  delay(20000);
  myservo.attach(9);
  myservo.write(0);
  delay(600);
  // myservo.write(0);
  // delay(500);
  myservo.detach();
}

void loop() {
   // Pause for 10 seconds (10000 milliseconds) before repeating
}