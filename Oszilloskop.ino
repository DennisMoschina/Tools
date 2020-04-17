const int numberOfReadings = 500;

unsigned char input0 = A0;
int readings[numberOfReadings];
int readingPtr;
int timeBase;
bool timeoutStatus;
String serialRead;


void setup() {
  Serial.begin(115200);
  Serial.setTimeout(20);
  pinMode(input0, INPUT);
  timeBase = 100;
  analogWrite(11, 100);
}

void loop() {
  for (readingPtr = 0; readingPtr < numberOfReadings; readingPtr++) {
    readings[readingPtr] = analogRead(input0);
    delayMicroseconds(timeBase);
  }

  timeoutStatus = true;

  while (timeoutStatus == true) {
    Serial.println("R?");
    serialRead = Serial.readString();
    if (serialRead == "K") {
      timeoutStatus = false;
    }
  }

  for (readingPtr = 0; readingPtr < numberOfReadings; readingPtr++) {
    Serial.write(highByte(readings[readingPtr] << 6));
  }
}
