int analogPin = A0;

int digitalIR = 50;
int digitalR = 52;

String command;
int timeStamp = 0;
int val;


void setup() {
    Serial1.begin(115200);
    Serial.begin(57600); 
    analogReadResolution(16);

    pinMode(digitalIR, OUTPUT);
    pinMode(digitalR, OUTPUT);

}

void loop() {
  digitalWrite(digitalIR, LOW);
  digitalWrite(digitalR, LOW);
  //pinMode(digitalIR, INPUT);
  //pinMode(digitalR, INPUT);

  sendData("B");

  //pinMode(digitalR, OUTPUT);
  digitalWrite(digitalR, HIGH);

  sendData("R");
  //delay(1000);

  digitalWrite(digitalR, LOW);
  //pinMode(digitalR, INPUT);


  sendData("B");
  
  //pinMode(digitalIR, OUTPUT);
  digitalWrite(digitalIR, HIGH);
  //delay(1000);

  sendData("I");
}


void sendData(String pType){
  val = 0;
  for (int i = 0; i <= 500; i++) {
    val += analogRead(analogPin);
  }
  val = val/500;
  timeStamp = millis();
  String msg = pType + ";" + String(val) + ";" + String(timeStamp) + "\n";
  int l = msg.length();
  //msg = String(l) + "l" + msg;
  char copy[24];
  msg.toCharArray(copy, 24);
  Serial1.write(copy);
  Serial.print(msg);
}
