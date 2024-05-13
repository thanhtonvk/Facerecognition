
void setup() {
  Serial.begin(280301);
  Serial.setTimeout(1);
}
int x;
void loop() {
  if (Serial.available() > 0) {
    x = Serial.readString().toInt();
    if (x == 1) {
      Serial.print("Mo o khoa 1");
      delay(2);
    }else if(x==2){
      Serial.print("Mo o khoa 2");
      delay(2);
    }
  }
}