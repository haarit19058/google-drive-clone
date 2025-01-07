
// void setup() {
//   Serial.begin(9600); // Initialize serial communication
// }

// void loop() {
  // flexValue = analogRead(flexPin); // Read the flex sensor value
  // Serial.print("Flex Sensor Value: "); // Print a label
  // Serial.println(flexValue); // Print the flex sensor value
//   delay(100); // Delay for 1 second
// }




#include <Servo.h> // Include the Servo library
const int flexPin = A0; // Analog pin connected to the flex sensor
int flexValue = 0; // Variable to store the flex sensor value

Servo servoMotor; // Create a servo object to control a servo motor
int servoPin = 9; // Define the pin to which the servo is connected

void setup() {
  servoMotor.attach(servoPin); // Attach the servo to the specified pin
  Serial.begin(9600); // Initialize serial communication
}

void loop() {
  // Move the servo to the 0 degree position
  flexValue = analogRead(flexPin);
  Serial.print("Flex Sensor Value: "); // Print a label
  Serial.println(flexValue*10); // Print the flex sensor value
  if (flexValue*10<5600){
  servoMotor.write(0);
  delay(100); // Wait for 1 second
  }
  else{
  // Move the servo to the 90 degree position
  servoMotor.write(90);
  delay(100); // Wait for 1 second
// 
  }
  
  // Move the servo to the 180 degree position
  // servoMotor.write(180);
  // delay(1000); // Wait for 1 second
}

