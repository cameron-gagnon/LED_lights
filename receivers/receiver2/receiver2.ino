// RECEIVER NUMBER 2

const int RECV_NUM = 2;
#include "Lights.h"
boolean ON = false;

//********* PIN SETUP *******************//
const unsigned short LED_PIN = 4;
Lights lights = Lights(LED_PIN);

//********* RECEIVER SETUP **************//
#include <printf.h>
#include <RF24.h>
#include <nRF24L01.h>

const unsigned short CE = 9;
const unsigned short CSN = 10;

RF24 radio(CE, CSN);

// address of the receiver, so we could have
// many receivers and we could still send to the
// correct one
const byte addresses[][6] = {"0Node", "1Node", "2Node", "3Node", "4Node"};


//********** SETUP *********************//
void setup() {
    Serial.begin(9600);

    // lcd/LED light pins
    pinMode(LED_PIN, OUTPUT);

    while (!Serial);

    radio.begin();
    radio.openReadingPipe(1, addresses[RECV_NUM]);
    radio.openWritingPipe(addresses[0]);

    radio.startListening();
    radio.printDetails();
}

//********** LOOP *********************//
void loop(){
    GetRFSignal();
}

/*
* Looks for "On" or "Off" text sent from
* the transmitter and sets the global ON
* variable accordingly
*/
void GetRFSignal(){

    if (radio.available()) {
        // array to read receiving chars in to
        int opcode;
        radio.read(&opcode, sizeof(int));
        
        Serial.print("OPCODE RECEIVED WAS: ");
        Serial.println(opcode);

        // set light variable on and off
        if (opcode & 0x10){
            lights.turnOn();
            pingBack(radio);
        } else if (opcode & 0x20){
            lights.turnOff();
            pingBack(radio);
        } else {
          pingBack(radio);
        }
    }
}

void pingBack(RF24 radio){
    radio.stopListening();
    int status = 2.1;
    radio.write(&status, sizeof(int));
    radio.startListening();
    Serial.println("Sent response to RPI");
}
