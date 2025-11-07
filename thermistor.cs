// ===== Thermistor Temperature Measurement =====
// Uses the Steinhart-Hart equation for high accuracy.
// Circuit: Thermistor in a voltage divider with a fixed resistor.
//
// Author: ChatGPT (GPT-5)
// Date: 2025

// ----------- CONFIGURATION -------------
#define THERMISTOR_PIN A0     // Analog input pin connected to voltage divider
#define SERIES_RESISTOR 10000  // Fixed resistor value in ohms (10kΩ typical)
#define NOMINAL_RESISTANCE 10000 // Thermistor resistance @ 25°C
#define NOMINAL_TEMPERATURE 25   // Reference temperature in °C
#define B_COEFFICIENT 3950       // Beta coefficient from datasheet
#define ADC_MAX 1023.0           // 10-bit ADC
#define VCC 5.0                  // Supply voltage (change if using 3.3V board)
// ----------------------------------------

// Optional: use Steinhart-Hart constants for more accuracy
// #define A 1.009249522e-03
// #define B 2.378405444e-04
// #define C 2.019202697e-07

void setup() {
  Serial.begin(9600);
  Serial.println("Thermistor Temperature Measurement");
}

void loop() {
  int adcValue = analogRead(THERMISTOR_PIN);

  // Convert ADC reading to voltage
  double voltage = adcValue * (VCC / ADC_MAX);

  // Compute thermistor resistance (voltage divider)
  double resistance = SERIES_RESISTOR * (VCC / voltage - 1.0);

  // ===== Simplified Beta Formula =====
  double steinhart;
  steinhart = resistance / NOMINAL_RESISTANCE;         // (R/Ro)
  steinhart = log(steinhart);                          // ln(R/Ro)
  steinhart /= B_COEFFICIENT;                          // 1/B * ln(R/Ro)
  steinhart += 1.0 / (NOMINAL_TEMPERATURE + 273.15);   // + (1/To)
  steinhart = 1.0 / steinhart;                         // Invert
  steinhart -= 273.15;                                 // Convert to °C

  // ===== If using full Steinhart-Hart equation =====
  // double lnR = log(resistance);
  // steinhart = 1.0 / (A + B * lnR + C * pow(lnR, 3));
  // steinhart -= 273.15;

  Serial.print("ADC = ");
  Serial.print(adcValue);
  Serial.print("  Resistance = ");
  Serial.print(resistance);
  Serial.print(" ohms  -->  Temperature = ");
  Serial.print(steinhart);
  Serial.println(" °C");

  delay(1000); // Wait 1 second between readings
}
