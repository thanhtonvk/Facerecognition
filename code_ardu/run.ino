byte ledPin[] = { 2, 3, 4, 5, 6, 7 };
byte pinCount;
void setup() {
  Serial.begin(280301);
  Serial.setTimeout(1);
  pinCount = sizeof(ledPin);
  for (int i = 0; i < pinCount; i += 1) {
    digitalWrite(ledPin[i], LOW);
    delay(500);
  }
}
int x;
void loop() {

  if (Serial.available() > 0) {
    x = Serial.readString().toInt();
    digitalWrite(ledPin[x - 1], HIGH);
    Serial.println('mo khoa '+ledPin[x - 1]);
    delay(3000);
    // đóng ổ khóa
    digitalWrite(ledPin[x - 1], LOW);  // Tắt đèn
    Serial.println('dong o khoa '+ledPin[x - 1]);
    delay(500);
  }
}