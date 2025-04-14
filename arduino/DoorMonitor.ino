/*
  This is the door monitor. All it does is listen for HIGH and LOW signal.
  There should be a python script waiting to read from the usb port if we can do it.
*/

//Pin for the door sensor
const int reedSwitchPin = 2; // Pin connected to the reed switch

//State
int reedSwitchState = 1;

//Previous state. Works like an atomic lock
int reedSwitchPrevious = 0;

//State to make sure we are acknowledging the door state update
boolean ackSend = false;

void setup() {
  Serial.begin(9600); // Initialize serial communication
  pinMode(reedSwitchPin, INPUT_PULLUP); // Set reed switch pin as input with internal pull-up resistor
  pinMode(LED_BUILTIN, OUTPUT); // Turn the LED on if you want to see things easier
  
  digitalWrite(LED_BUILTIN, LOW);
  
  
  //Do something here to check what state the door is in initially
  reedSwitchState = digitalRead(reedSwitchPin);
  
  //Send an initial message to clear out the port
  Serial.println("<Now Sending Content>");
  
  if(reedSwitchState == LOW){
    Serial.println("<Closed>");
  }
  else{
    Serial.println("<Open>");
  }
}

void loop() {
  reedSwitchPrevious = reedSwitchState;
  reedSwitchState = digitalRead(reedSwitchPin); // Read the state of the reed switch pin

  //When in a LOW state the reed switch is sitting next to the magnet and the door is CLOSED
  
  
  //We start with the door set as OPEN or CLOSED initially so you have to close or open the circuit to see results
  //OPEN STATE
  if (reedSwitchState == LOW && reedSwitchPrevious == HIGH) {
    //Closed door
    
    Serial.println("<Closed>"); // Print message if reed switch is closed (ON)
    digitalWrite(LED_BUILTIN, LOW);
    ackSend= true;
    
  } 
  //CLOSED STATE
  else if(reedSwitchState == HIGH && reedSwitchPrevious == LOW) {
    Serial.println("<Open>"); // Print message if reed switch is open (OFF)
    //digitalWrite(LED_BUILTIN, HIGH);
    ackSend= true;
  }
  
  
  //Look and see that the ArduinoListener.py acked our message
  if(ackSend && Serial.available() > 0){

    
    //Read from the serial port character by character until the new line char appears
    String cur = Serial.readString();
    
    cur.trim();


    // Light the LED if needed
    if(cur.equals("<Alert>")){
      digitalWrite(LED_BUILTIN, HIGH);
    }


    

    // we have read all of the string so make ackSend false and end this loop
    ackSend = false;

  }

  delay(500); // Delay for stability. If we read too fast it gets hard to consistently read messages
}
