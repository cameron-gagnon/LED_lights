/*
   Copyright (C) 2011 J. Coliz <maniacbug@ymail.com>

   This program is free software; you can redistribute it and/or
   modify it under the terms of the GNU General Public License
   version 2 as published by the Free Software Foundation.

   03/17/2013 : Charles-Henri Hallard (http://hallard.me)
   Modified to use with Arduipi board http://hallard.me/arduipi
   Changed to use modified bcm2835 and RF24 library
   TMRh20 2014 - Updated to work with optimized RF24 Arduino library

*/

/**
 * Example RF Radio Ping Pair
 *
 * This is an example of how to use the RF24 class on RPi, communicating to an Arduino running
 * the GettingStarted sketch.
 */

#include <cstdlib>
#include <iostream>
#include <sstream>
#include <string>
#include <unistd.h>
#include <RF24/RF24.h>

using namespace std;
//
// Hardware configuration
// Configure the appropriate pins for your connections

/****************** Raspberry Pi ***********************/

// Radio CE Pin, CSN Pin, SPI Speed


// Assign a unique identifier for this node, 0 or 1
bool radioNumber = 1;

// Radio pipe addresses for the 2 nodes to communicate.
const uint8_t pipes[][6] = {"1Node","2Node"};

RF24 setup();
void process(RF24 radio);
void send(RF24 radio, int opcode);

int main(int argc, char** argv){

    RF24 radio = setup();
    process(radio);

    return 0;
}

/* REQUIRES: nRF240l+ module be correctly wired to send packets
 * MODIFIES: radio configuration
 * EFFECTS:  Sets up the radio variable to be able to send packets
 */
RF24 setup(){

    // RPi generic:
    RF24 *radio = new RF24(25, 0);

    // Setup and configure rf radio
    radio->begin();

    // optionally, increase the delay between retries and # of retries
    radio->setRetries(15,15);
    // Dump the configuration of the rf unit for debugging
    radio->printDetails();

    // this radio will always be the sender so we open these pipes for
    // reading/writing
    radio->openWritingPipe(pipes[1]);
    radio->openReadingPipe(1,pipes[0]);

    radio->startListening();

    return *radio;
}

/* REQUIRES: Radio be set up and able to communicate
 * MODIFIES: Nothing
 * EFFECTS:  Digests the opcode received from the Python back end and then
 *           sends the corresponding signals to the Arduino's that are
 *           supposed to receive it.
 */
void process(RF24 radio){

    int opcode;
    cin >> hex >> opcode;
    cout << "Got signal: " << opcode << "\n";

    // First, stop listening so we can talk.
    radio.stopListening();

    /*
    // could be used to reduce duplicate code
      for (int i = 0; i < NUM_ARDUINOS; ++i){
        if (opcode & ARDUINO_MASKS[i]){
            send(opcode);
        }
    }*/

    // Arduino 1 was specified
    if (opcode & 0x01){
        send(radio, opcode);
    }

    // Arduino 2 was specified
/*    if (opcode & 0x02){
        send(radio, opcode);
    }

    // Arduino 3 was specified
    if (opcode & 0x04){
        send(radio, opcode);
    }

    // Arduino 4 was specified
    if (opcode & 0x08){
        send(radio, opcode);
    }
*/

}

void send(RF24 radio, int opcode){

    // Take the time, and send it. This will block until complete
    printf("Now sending...\n");
    bool ok = radio.write( &opcode, sizeof(int) );

    if (!ok){
        printf("failed.\n");
    }
    // Now, continue listening
    radio.startListening();

    // Wait here until we get a response, or timeout (250ms)
    unsigned long started_waiting_at = millis();
    bool timeout = false;
    while ( !radio.available() && !timeout ) {
        if (millis() - started_waiting_at > 250 ){
            timeout = true;
        }
    }


    // Describe the results
    if (timeout) {
        printf("Failed, response timed out.\n");

    } else {
        // Grab the response, compare, and send to debugging spew
        unsigned long got_time;
        radio.read( &got_time, sizeof(unsigned long) );

        // Spew it
        printf("Got response %lu, round-trip delay: %lu\n",
               got_time, millis() - got_time);
    }
    sleep(1);

}
