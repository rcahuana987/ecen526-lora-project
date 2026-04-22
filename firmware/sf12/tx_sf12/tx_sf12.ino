#include <heltec_unofficial.h>

// ===================== USER SETTINGS =====================
float LORA_FREQ_MHZ = 915.0;   // 915.0 for US, 868.0 for EU
int LORA_SF = 12;
float LORA_BW_KHZ = 125.0;
int LORA_CR = 5;               // 5 = 4/5
int LORA_TX_POWER = 14;
int LORA_PREAMBLE = 8;
unsigned long TX_INTERVAL_MS = 200;   // 5 packets/sec
const uint8_t PAYLOAD_SIZE = 20;
// ========================================================

uint32_t seq_num = 0;
unsigned long last_tx = 0;

void setup() {
  heltec_setup();
  delay(500);

  Serial.println("TX booting...");
  display.clear();
  display.drawString(0, 0, "TX booting...");
  display.display();

  int state = radio.begin();
  if (state != RADIOLIB_ERR_NONE) {
    Serial.print("radio.begin failed, code=");
    Serial.println(state);
    while (true) delay(1000);
  }

  state = radio.setFrequency(LORA_FREQ_MHZ);
  if (state != RADIOLIB_ERR_NONE) {
    Serial.print("setFrequency failed, code=");
    Serial.println(state);
    while (true) delay(1000);
  }

  state = radio.setBandwidth(LORA_BW_KHZ);
  if (state != RADIOLIB_ERR_NONE) {
    Serial.print("setBandwidth failed, code=");
    Serial.println(state);
    while (true) delay(1000);
  }

  state = radio.setSpreadingFactor(LORA_SF);
  if (state != RADIOLIB_ERR_NONE) {
    Serial.print("setSpreadingFactor failed, code=");
    Serial.println(state);
    while (true) delay(1000);
  }

  state = radio.setCodingRate(LORA_CR);
  if (state != RADIOLIB_ERR_NONE) {
    Serial.print("setCodingRate failed, code=");
    Serial.println(state);
    while (true) delay(1000);
  }

  state = radio.setOutputPower(LORA_TX_POWER);
  if (state != RADIOLIB_ERR_NONE) {
    Serial.print("setOutputPower failed, code=");
    Serial.println(state);
    while (true) delay(1000);
  }

  state = radio.setPreambleLength(LORA_PREAMBLE);
  if (state != RADIOLIB_ERR_NONE) {
    Serial.print("setPreambleLength failed, code=");
    Serial.println(state);
    while (true) delay(1000);
  }

  Serial.println("TX ready");
  Serial.println("time_ms,role,seq,payload_len,sf,bw_khz,cr,tx_power_dbm");

  display.clear();
  display.drawString(0, 0, "TX ready");
  display.drawString(0, 12, "Freq: " + String(LORA_FREQ_MHZ, 1));
  display.drawString(0, 24, "SF: " + String(LORA_SF));
  display.display();
}

void loop() {
  heltec_loop();

  unsigned long now = millis();
  if (now - last_tx < TX_INTERVAL_MS) {
    return;
  }
  last_tx = now;

  uint8_t payload[PAYLOAD_SIZE];
  payload[0] = (seq_num >> 24) & 0xFF;
  payload[1] = (seq_num >> 16) & 0xFF;
  payload[2] = (seq_num >> 8) & 0xFF;
  payload[3] = seq_num & 0xFF;

  for (int i = 4; i < PAYLOAD_SIZE; i++) {
    payload[i] = (uint8_t)((seq_num + i) & 0xFF);
  }

  int state = radio.transmit(payload, PAYLOAD_SIZE);

  Serial.print(millis());
  Serial.print(",TX,");
  Serial.print(seq_num);
  Serial.print(",");
  Serial.print(PAYLOAD_SIZE);
  Serial.print(",");
  Serial.print(LORA_SF);
  Serial.print(",");
  Serial.print(LORA_BW_KHZ);
  Serial.print(",");
  Serial.print(LORA_CR);
  Serial.print(",");
  Serial.println(LORA_TX_POWER);

  display.clear();
  display.drawString(0, 0, "TX OK");
  display.drawString(0, 12, "Seq: " + String(seq_num));
  display.drawString(0, 24, "SF: " + String(LORA_SF));
  display.drawString(0, 36, "BW: " + String(LORA_BW_KHZ));
  display.display();

  seq_num++;
}
