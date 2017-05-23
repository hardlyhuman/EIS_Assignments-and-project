#include <SoftwareSerial.h>
#include<String.h >
#define DEBUG true
 
SoftwareSerial esp8266(4,5); // make RX Arduino line is pin 2, make TX Arduino line is pin 3.
                             // This means that you need to connect the TX line from the esp to the Arduino's pin 2
                             // and the RX line from the esp to the Arduino's pin 3
byte statusLed    = 13;

byte sensorInterrupt = 0;  // 0 = digital pin 2
byte sensorPin       = 2;

float calibrationFactor = 4.5;

volatile byte pulseCount;  

float flowRate;
unsigned int flowMilliLitres;
unsigned long totalMilliLitres;

unsigned long oldTime;
void setup()
{
  Serial.begin(9600);
  esp8266.begin(57600); // your esp's baud rate might be different
  
 
  
  sendData("AT+RST\r\n",2000,DEBUG); // reset module
  sendData("AT+CWMODE=3\r\n",1000,DEBUG); // configure as access point
  sendData("AT+CIFSR\r\n",1000,DEBUG); // get ip address
  sendData("AT+CIPMUX=1\r\n",1000,DEBUG); // configure for multiple connections
  sendData("AT+CIPSERVER=1,1336\r\n",1000,DEBUG); // turn on server on port 80
  pinMode(statusLed, OUTPUT);
  digitalWrite(statusLed, HIGH);  // We have an active-low LED attached
  
  pinMode(sensorPin, INPUT);
  digitalWrite(sensorPin, HIGH);

  pulseCount        = 0;
  flowRate          = 0.0;
  flowMilliLitres   = 0;
  totalMilliLitres  = 0;
  oldTime           = 0;

  attachInterrupt(sensorInterrupt, pulseCounter, FALLING);
}


      
   //totalMilliLitres += 1;

void loop()
{sensorInterrupt = 0;
  if(esp8266.available()) // check if the esp is sending a message 
  {
    /*
    while(esp8266.available())
    {
      // The esp has data so display its output to the serial window 
      char c = esp8266.read(); // read the next character.
      Serial.write(c);
    } */
    
    if(esp8266.find("+IPD,"))
    {
     delay(1000);
 
     int connectionId = esp8266.read()-48; // subtract 48 because the read() function returns 
     while(1){                                      // the ASCII decimal value and 0 (the first decimal number) starts at 48
      if((millis() - oldTime) > 1000)    // Only process counters once per second
  { 
              //  detachInterrupt(sensorInterrupt);
        detachInterrupt(sensorInterrupt);
     flowRate = ((1000.0 / (millis() - oldTime)) * pulseCount) / calibrationFactor;
    
   oldTime = millis();
   flowMilliLitres = (flowRate / 60) * 1000;
   //  Add();
      totalMilliLitres += flowMilliLitres;
    Serial.print(totalMilliLitres); 
        pulseCount = 0;
     attachInterrupt(sensorInterrupt, pulseCounter, FALLING);
  //detachInterrupt(sensorInterrupt);
  
   String webpage = String(totalMilliLitres);
     String cipSend = "AT+CIPSEND=";
     cipSend += connectionId;
     cipSend += ",";
     cipSend +=webpage.length();
     cipSend +="\r\n";
     
     sendData(cipSend,1000,DEBUG);
     sendData(webpage,1000,DEBUG);
  } 
  delay(100);
  esp8266.println("AT+CIPCLOSE=0");
  delay(100);
    }  
     //webpage="<button>LED2</button>";
     
     //cipSend = "AT+CIPSEND=";
     //cipSend += connectionId;
     //cipSend += ",";
     //cipSend +=webpage.length();
     //cipSend +="\r\n";
     
     //sendData(cipSend,1000,DEBUG);
     //sendData(webpage,1000,DEBUG);
 
     //String closeCommand = "AT+CIPCLOSE="; 
     //closeCommand+=connectionId; // append connection id
     //closeCommand+="\r\n";
     
    }   //sendData(closeCommand,3000,DEBUG);
    }
  }

 
 
String sendData(String command, const int timeout, boolean debug)
{
    String response = "";
    
    esp8266.print(command); // send the read character to the esp8266
    
    long int time = millis();
    
    while( (time+timeout) > millis())
    {
      while(esp8266.available())
      {
        
        // The esp has data so display its output to the serial window 
        char c = esp8266.read(); // read the next character.
        response+=c;
      }  
    }
    
    if(debug)
    {
      Serial.print(response);
    }
    
    return response;
}


void pulseCounter()
{
  // Increment the pulse counter
  pulseCount++;
}
