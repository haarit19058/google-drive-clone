void setup() {
  // put your setup code here, to run once:
  pinMode(0,OUTPUT);
  // Serial.begin(9600);
}

void loop() {
  int val = analogRead(A0);
  Serial.println(val);
  // hello guys 
  
  if (val < 200) {
    digitalWrite(0, HIGH); // Turn on LED
  } else {
    digitalWrite(0, LOW); // Turn off LED
  }
  
  // digitalWrite(0, LOW);
  // delay(500);
  // digitalWrite(0, HIGH);
  // delay(500);

  delay(100); // Add a small delay to prevent rapid readings
}

