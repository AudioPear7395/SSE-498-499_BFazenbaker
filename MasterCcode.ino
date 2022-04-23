//Master Code
//Benjamin Fazenbaker
//Oxygen Sensor + CO2
#include "DFRobot_OxygenSensor.h"
#include <Wire.h>
#include "Adafruit_SGP30.h"
//radiation library
#include <avr/dtostrf.h>

#define COLLECT_NUMBER    10             // collect number, the collection range is 1-100.
#define Oxygen_IICAddress ADDRESS_3

Adafruit_SGP30 sgp;
DFRobot_OxygenSensor Oxygen;
//SGP
uint32_t getAbsoluteHumidity(float temperature, float humidity) {
    // approximation formula from Sensirion SGP30 Driver Integration chapter 3.15
    const float absoluteHumidity = 216.7f * ((humidity / 100.0f) * 6.112f * exp((17.62f * temperature) / (243.12f + temperature)) / (273.15f + temperature)); // [g/m^3]
    const uint32_t absoluteHumidityScaled = static_cast<uint32_t>(1000.0f * absoluteHumidity); // [mg/m^3]
    return absoluteHumidityScaled;
}

int counter = 0;

//radiation stuff
int signPin = 2; //Radiation Pulse (Yellow)
int noisePin = 5; //Vibration Noise Pulse (White)

const double alpha = 53.032; // cpm = uSv x alpha

int index2 = 0; //Number of loops
char msg[256] = ""; //Message buffer for serial output

int signCount = 0; //Counter for Radiation Pulse
int noiseCount = 0; //Counter for Noise Pulse

int sON = 0; //Lock flag for Radiation Pulse
int nON = 0; //Lock flag for Noise Puls

double cpm = 0; //Count rate [cpm] of current
double cpmHistory[200]; //History of count rates
int cpmIndex = 0; //Position of current count rate on cpmHistory[]
int cpmIndexPrev = 0; //Flag to prevent duplicative counting

//Timing Settings for Loop Interval
int prevTime = 0;
int currTime = 0;

int totalSec = 0; //Elapsed time of measurement [sec]
int totalHour = 0; //Elapsed time of measurement [hour]

//Time settings for CPM calcuaration
int cpmTimeMSec = 0;
int cpmTimeSec = 0;
int cpmTimeMin = 0;

//String buffers of float values for serial output
char cpmBuff[20];
char uSvBuff[20];
char uSvdBuff[20];
int radtim;

//combining variable
String Combiner;

void setup() 
{
  //
  
  //Sending Data
  radtim=millis();
  Serial1.begin(115200);
  //Oxygen
  Serial.begin(9600);
  while(!Oxygen.begin(Oxygen_IICAddress)) {
    Serial.println("I2c device number error !");
    delay(1000);
  }
  Serial.println("I2c connect success !");
//SGP

  Serial.println("SGP30 test");

  if (! sgp.begin()){
    Serial.println("Sensor not found :(");
    //while (1);
  }
  Serial.print("Found SGP30 serial #");
  Serial.print(sgp.serialnumber[0], HEX);
  Serial.print(sgp.serialnumber[1], HEX);
  Serial.println(sgp.serialnumber[2], HEX);

  //radiation stuff
  
  //PIN setting for Radiation Pulse
  pinMode(signPin, INPUT);
  digitalWrite(signPin, HIGH);

  //PIN setting for Noise Pulse
  pinMode(noisePin, INPUT);
  digitalWrite(noisePin, HIGH);

  //CSV-formatting for serial output (substitute , for _)
  Serial1.println("hour[h]_sec[s]_count_cpm_uSv/h_uSv/hError");

  //Initialize cpmHistory[]
  for (int i = 0; i < 200; i++ )
  {
    cpmHistory[i] = 0;
  }

  //Get start time of a loop
  prevTime = millis();
}

void radiation_counter()
{
   // Raw data of Radiation Pulse: Not-detected -> High, Detected -> Low
  int sign = digitalRead(signPin);

  // Raw data of Noise Pulse: Not-detected -> Low, Detected -> High
  int noise = digitalRead(noisePin);

  //Radiation Pulse normally keeps low for about 100[usec]
  if (sign == 0 && sON == 0)
  { //Deactivate Radiation Pulse counting for a while
    sON = 1;
    signCount++;
  } else if (sign == 1 && sON == 1) {
    sON = 0;
  }

  //Noise Pulse normally keeps high for about 100[usec]
  if (noise == 1 && nON == 0)
  { //Deactivate Noise Pulse counting for a while
    nON = 1;
    noiseCount++;
  } else if (noise == 0 && nON == 1) {
    nON = 0;
  }

  //Output readings to serial port, after 10000 loops CHANGED TO 100 FOR FASTER INCREMENTS
  if (index2 == 100) //About 160-170 msec in Arduino Nano(ATmega328)
  {
    //Get current time
    currTime = millis();

    //No noise detected in 10000 loops
    if (noiseCount == 0)
    {
      //Shift an array for counting log for each 6 sec.
      if ( totalSec % 6 == 0 && cpmIndexPrev != totalSec)
      {
        cpmIndexPrev = totalSec;
        cpmIndex++;

        if (cpmIndex >= 200)
        {
          cpmIndex = 0;
        }

        if (cpmHistory[cpmIndex] > 0)
        {
          cpm -= cpmHistory[cpmIndex];
        }
        cpmHistory[cpmIndex] = 0;
      }

      //Store count log
      cpmHistory[cpmIndex] += signCount;
      //Add number of counts
      cpm += signCount;

      //Get ready time for 10000 loops
      cpmTimeMSec += abs(currTime - prevTime);
      //Transform from msec. to sec. (to prevent overflow)
      if (cpmTimeMSec >= 1000)
      {
        cpmTimeMSec -= 1000;
        //Add measurement time to calcurate cpm readings (max=20min.)
        if ( cpmTimeSec >= 20 * 60 )
        {
          cpmTimeSec = 20 * 60;
        } else {
          cpmTimeSec++;
        }

        //Total measurement time
        totalSec++;
        //Transform from sec. to hour. (to prevent overflow)
        if (totalSec >= 3600)
        {
          totalSec -= 3600;
          totalHour++;
        }
      }

      //Elapsed time of measurement (max=20min.)
      double min = cpmTimeSec / 60.0;
      if (min != 0)
      {
        //Calculate cpm, uSv/h and error of uSv/h
        dtostrf(cpm / min, -1, 0, cpmBuff);
        dtostrf(cpm / min / alpha, -1, 3, uSvBuff);
        dtostrf(sqrt(cpm) / min / alpha, -1, 3, uSvdBuff);
      } else {
        //Devision by zero
        dtostrf(0, -1, 3, cpmBuff);
        dtostrf(0, -1, 3, uSvBuff);
        dtostrf(0, -1, 3, uSvdBuff);
      }

      //Create message for serial port
      sprintf(msg, "%d,%d.%03d,%d,%s,%s,%s",
              totalHour, totalSec,
              cpmTimeMSec,
              signCount,
              cpmBuff,
              uSvBuff,
              uSvdBuff
             );

    }

    //Initialization for next 10000 loops
    prevTime = currTime;
    signCount = 0;
    noiseCount = 0;
    index2 = 0;
  }
  index2++;
}


void loop()
{
  //Combiner stuff
  Combiner = "";
  //Radiation
  radiation_counter();
  
  if (millis()-radtim>=1000){
  Serial.print("Radiation Counted as:");
  Serial.println(cpmBuff);
  //Oxygen
  radtim=millis();
  float oxygenData = Oxygen.ReadOxygenData(COLLECT_NUMBER);
  Serial.print(" Oxygen concentration is ");
  Serial.print(oxygenData);
  Serial.println(" %vol");
  //SGP
   if (! sgp.IAQmeasure()) {
    Serial.println("Measurement failed");
    return;
  }
  Combiner.concat(sgp.TVOC);
  Combiner.concat(",");
  Combiner.concat(sgp.eCO2);
  Combiner.concat(",");
  Combiner.concat(oxygenData);
  Combiner.concat(",");
  Combiner.concat(cpmBuff);
  Combiner.concat(",");
  Combiner.concat("##");
  Serial1.print(Combiner);
  Serial1.flush();

  if (! sgp.IAQmeasureRaw()) {
    Serial.println("Raw Measurement failed");
    return;
  }
  Serial.print("Raw H2 "); Serial.print(sgp.rawH2); Serial.print(" \t");
  Serial.print("Raw Ethanol "); Serial.print(sgp.rawEthanol); Serial.println("");
 

  counter++;
  if (counter == 30) {
    counter = 0;

    uint16_t TVOC_base, eCO2_base;
    if (! sgp.getIAQBaseline(&eCO2_base, &TVOC_base)) {
      Serial.println("Failed to get baseline readings");
      return;
    }
    Serial.print("****Baseline values: eCO2: 0x"); Serial.print(eCO2_base, HEX);
    Serial.print(" & TVOC: 0x"); Serial.println(TVOC_base, HEX);
  }
  }
}
