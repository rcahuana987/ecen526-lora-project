#include <heltec_unofficial.h>

// ===================== USER SETTINGS =====================
float LORA_FREQ_MHZ = 915.0;   // Must match TX
int LORA_SF = 7;               // Must match TX
float LORA_BW_KHZ = 125.0;     // Must match TX
int LORA_CR = 5;               // Must match TX
int LORA_TX_POWER = 14;        // Logged for reference
int LORA_PREAMBLE = 8;
const uint8_t MAX_PACKET_SIZE = 64;
// ========================================================

uint32_t received_count = 0;
uint32_t missed_count = 0;
int32_t expected_seq = 0;

void setup() {
  heltec_setup();
  delay(500);

  Serial.println("RX booting...");
  display.clear();
  display.drawString(0, 0, "RX booting...");
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

  Serial.println("RX ready");
  Serial.println("time_ms,seq,payload_len,sf,bw_khz,cr,tx_power_dbm,rssi_dbm,snr_db,received_total,missed_total");

  display.clear();
  display.drawString(0, 0, "RX ready");
  display.drawString(0, 12, "Freq: " + String(LORA_FREQ_MHZ, 1));
  display.drawString(0, 24, "SF: " + String(LORA_SF));
  display.display();
}

void loop() {
  heltec_loop();

  uint8_t data[MAX_PACKET_SIZE];
  int state = radio.receive(data, MAX_PACKET_SIZE);

  if (state == RADIOLIB_ERR_NONE) {
    int packet_len = radio.getPacketLength();

    if (packet_len >= 4) {
      uint32_t seq =
        ((uint32_t)data[0] << 24) |
        ((uint32_t)data[1] << 16) |
        ((uint32_t)data[2] << 8)  |
        ((uint32_t)data[3]);

      if (received_count == 0) {
        expected_seq = seq;
      }

      if ((int32_t)seq > expected_seq) {
        missed_count += (seq - expected_seq);
      }

      expected_seq = seq + 1;
      received_count++;

      float rssi = radio.getRSSI();
      float snr = radio.getSNR();

      Serial.print(millis());
      Serial.print(",");
      Serial.print(seq);
      Serial.print(",");
      Serial.print(packet_len);
      Serial.print(",");
      Serial.print(LORA_SF);
      Serial.print(",");
      Serial.print(LORA_BW_KHZ);
      Serial.print(",");
      Serial.print(LORA_CR);
      Serial.print(",");
      Serial.print(LORA_TX_POWER);
      Serial.print(",");
      Serial.print(rssi);
      Serial.print(",");
      Serial.print(snr);
      Serial.print(",");
      Serial.print(received_count);
      Serial.print(",");
      Serial.println(missed_count);

      display.clear();
      display.drawString(0, 0, "RX OK");
      display.drawString(0, 12, "Seq: " + String(seq));
      display.drawString(0, 24, "RSSI: " + String(rssi, 1));
      display.drawString(0, 36, "SNR: " + String(snr, 1));
      display.display();
    }
  }
}
