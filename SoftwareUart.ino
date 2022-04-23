//char mystr[10]; //Initialized variable to store recieved data
// Include RadioHead Amplitude Shift Keying Library
#include <RH_ASK.h>
// Include dependant SPI Library 
#include <SPI.h> 
RH_ASK rf_driver;
//#include <SoftwareSerial.h>
//SoftwareSerial Serial2(4,5);
UART Serial2(4,5,NC,NC);

String sensor1;
String sensor2;
String msg = "";
char msg2[50] = "";
void setup() {
  // Begin the Serial at 9600 Baud
  Serial1.begin(115200); //UART 0 Pins 0-1 on Main Pico
  Serial.begin(9600);
  Serial2.begin(9600); //UART 1 Pins 4-5 on Main Pico

  Serial1.setTimeout(20);

  Serial2.setTimeout(20);

  //sending setup
  // Initialize ASK Object
  rf_driver.init();
}

void serial1Flush(){
  while(Serial1.available() > 0){
    char t = Serial1.read();
  }
}
void serial2Flush(){
  while(Serial2.available() > 0){
    char t = Serial2.read();
  }
}

void loop() {
  /*while (Serial1.available() > 0) {
    // read the incoming byte:
    //Serial1.read(mystr,6);
    Serial.print((char)Serial1.read());  
    //Serial.println(mystr); //Print data on Serial Monitor
}

delay(250);

    while (Serial2.available() > 0) {
    // read the incoming byte:
    //Serial1.read(mystr,6);
    Serial.print((char)Serial2.read());  
    //Serial.println(mystr); //Print data on Serial Monitor
    }
//else{
  //Serial.println();
  //delay(1000);
//}*/

//Serial.print(Serial1.readString());
//Serial.print(Serial2.readString());
msg = "";
//Sensor 1 = Arduino
if (Serial1.available()){
  sensor1 = Serial1.readStringUntil('#');
  serial1Flush();
  //Serial1.flush();
  //Serial.println(sensor1);
}
//Sensor 2 = Python
if (Serial2.available()){
  sensor2 = Serial2.readStringUntil('|');
  serial2Flush();
  //Serial2.flush();
  //Serial.println(sensor2);
}
msg = sensor1 + sensor2;
msg.toCharArray(msg2,50);

//Serial.println(msg2);


//sending stuff via radio
//const char *msg = "lol";
    rf_driver.send((uint8_t *)msg2, strlen(msg2));
    //rf_driver.send(msg2,strlen(msg2));
    rf_driver.waitPacketSent();
    Serial.println(msg2);
    delay(1000);
}
