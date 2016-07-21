#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

class Lights {
  private:
    const unsigned short LED_PIN;
    Adafruit_NeoPixel strip;

    void steady(int R, int G, int B) {
      for (uint16_t i = 0; i < strip.numPixels(); ++i) {
        strip.setPixelColor(i, strip.Color(R, G, B));
      }
      strip.show();
    }

  public:
    Lights(const unsigned short in_led_pin): LED_PIN(in_led_pin) {
      strip = Adafruit_NeoPixel(180, 6, NEO_GRB + NEO_KHZ800);
      strip.begin();
    };

    void turnOff() {
      Serial.print("Turning off");
      digitalWrite(LED_PIN, LOW);
      steady(0, 0, 0);
    }

    void turnOn() {
      Serial.print("Turning on");
      digitalWrite(LED_PIN, HIGH);
      steady(127, 127, 127);
    }

    void wipe() {
      Serial.print("Wiping");
      colorWipe(strip.Color(255, 0, 0), 50); // Red
      colorWipe(strip.Color(0, 255, 0), 50); // Green
      colorWipe(strip.Color(0, 0, 255), 50); // Blue
    }

    void cycle() {
      Serial.print("Cycling");
      rainbow(20);
    }

    void chase() {
      Serial.print("Chasing");
      theaterChase(strip.Color(127, 127, 127), 50); // White
    }


    // Fill the dots one after the other with a color
    void colorWipe(uint32_t c, uint8_t wait) {
      for (uint16_t i = 0; i < strip.numPixels(); i++) {
        strip.setPixelColor(i, c);
        strip.show();
        delay(wait);
      }
    }

    // uneven distribution of rainbow, not evenly distributed throughout strip
    void rainbow(uint8_t wait) {
      uint16_t i, j;

      for (j = 0; j < 256; j++) {
        for (i = 0; i < strip.numPixels(); i++) {
          strip.setPixelColor(i, Wheel((i + j) & 255));
        }
        strip.show();
        delay(wait);
      }
    }

    // Slightly different, this makes the rainbow equally distributed throughout
    void rainbowCycleEqual(uint8_t wait) {
      uint16_t i, j;

      for (j = 0; j < 256 * 5; j++) { // 5 cycles of all colors on wheel
        for (i = 0; i < strip.numPixels(); i++) {
          strip.setPixelColor(i, Wheel(((i * 256 / strip.numPixels()) + j) & 255));
        }
        strip.show();
        delay(wait);
      }
    }

    //Theatre-style crawling lights.
    void theaterChase(uint32_t c, uint8_t wait) {
      for (int j = 0; j < 10; j++) { //do 10 cycles of chasing
        for (int q = 0; q < 3; q++) {
          for (uint16_t i = 0; i < strip.numPixels(); i = i + 3) {
            strip.setPixelColor(i + q, c);  //turn every third pixel on
          }
          strip.show();

          delay(wait);

          for (uint16_t i = 0; i < strip.numPixels(); i = i + 3) {
            strip.setPixelColor(i + q, 0);      //turn every third pixel off
          }
        }
      }
    }

    //Theatre-style crawling lights with rainbow effect
    void theaterChaseRainbow(uint8_t wait) {
      for (int j = 0; j < 256; j++) {   // cycle all 256 colors in the wheel
        for (int q = 0; q < 3; q++) {
          for (uint16_t i = 0; i < strip.numPixels(); i = i + 3) {
            strip.setPixelColor(i + q, Wheel( (i + j) % 255)); //turn every third pixel on
          }
          strip.show();

          delay(wait);

          for (uint16_t i = 0; i < strip.numPixels(); i = i + 3) {
            strip.setPixelColor(i + q, 0);      //turn every third pixel off
          }
        }
      }
    }
    // Input a value 0 to 255 to get a color value.
    // The colours are a transition r - g - b - back to r.
    uint32_t Wheel(byte WheelPos) {
      WheelPos = 255 - WheelPos;
      if (WheelPos < 85) {
        return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
      }
      if (WheelPos < 170) {
        WheelPos -= 85;
        return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
      }
      WheelPos -= 170;
      return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
    }
};
