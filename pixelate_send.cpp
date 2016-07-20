/**
 * Communicate with Arduino's from a Raspberry Pi using specific opcodes
 * designed for this project.
 *
 */

#include <cstdlib>
#include <iostream>
#include <sstream>
#include <string>
#include <unistd.h>
#include <RF24/RF24.h>

using namespace std;

// Assign a unique identifier for this node, 0 or 1
bool radioNumber = 1;

// Radio pipe addresses for the 2 nodes to communicate.
const uint8_t pipes[][6] = {"0Node", "1Node","2Node"};//, "3Node"};//, "4Node"};
const int ARDUINO_MASKS[] = {0x01, 0x02};//, 0x04};//, 0x08};
const int NUM_ARDUINOS = 2; // will be 4

RF24 setup();
void process(RF24 radio, char** argv);
void send(RF24 radio, int opcode, int i);

int main(int argc, char** argv){

    RF24 radio = setup();
    process(radio, argv);

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
    //radio->printDetails();

    // This radio will always be the sender so we open this pipe for
    // reading. Pipes will be opened for writing to on an as needed
    // basis.
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
void process(RF24 radio, char** argv){

    // use argv[1] because our program is called like:
    //     sudo ./pixelate_send 0x1f
    // where sudo does not count as an input to the program, just
    // ./pixelate_send and 0x1f, so argv[1] is 0x1f
    // then convert the hex string to an integer
    istringstream iss(argv[1]);
    int opcode;
    iss >> hex >> opcode;
    cout << "Got signal: " << opcode << endl;

    for (int i = 0; i < NUM_ARDUINOS; ++i){
        if (opcode & ARDUINO_MASKS[i]){
            cout << "[" << (i + 1) << "] Sending opcode: " << opcode << "\n";
            send(radio, opcode, i);
        }
    }


}

void send(RF24 radio, int opcode, int i){
    // First, stop listening so we can talk.
    radio.stopListening();

    // offset because 0node is ourself (the rpi)
    radio.openWritingPipe(pipes[i + 1]);

    // Take the time, and send it. This will block until complete
    printf("Now sending...\n");
    bool ok = radio.write( &opcode, sizeof(int) );

    if (!ok){
        printf("NO RESPONSE/FAILED TO WRITE.\n");
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

}
