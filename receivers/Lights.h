class Lights{
  const unsigned short LED_PIN;

 public:
  Lights(const unsigned short in_led_pin):LED_PIN(in_led_pin){};

  void turnOff(){
    digitalWrite(LED_PIN, LOW);
  }
  
  void turnOn(){
    digitalWrite(LED_PIN, HIGH);
  }
};
