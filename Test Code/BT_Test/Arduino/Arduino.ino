//Use this code to test BT communication between Arduino Car and Raspberry Pi Car
void setup() {
  Serial.begin( 9600 );
}
void loop() {
  // listen for the data from raspberry pi
  if ( Serial.available() > 0 ) {
    // read a numbers from serial port
    int inputVal = Serial.parseInt();
    if (inputVal > 0) {
        Serial.print("Your input is: ");
        Serial.println(String(inputVal));
    }
  }
}
