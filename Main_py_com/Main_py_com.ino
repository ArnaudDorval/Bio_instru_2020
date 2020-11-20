//#include <SoftwareSerial.h>
//SoftwareSerial myBluetooth(10,11); //RX TX

int analogPin = A0;

int digitalIR = 50;
int digitalR = 52;

int digitalGo = 31;
int digitalWait = 30;

String command;
int timeStamp = 0;
int val;
 
void setup() {
    Serial.begin(57600);
    Serial1.begin(115200); 
    analogReadResolution(16);

    pinMode(digitalIR, OUTPUT);
    pinMode(digitalR, OUTPUT);

    pinMode(digitalGo, OUTPUT);
    pinMode(digitalWait, OUTPUT);

    digitalWrite(digitalIR, LOW);
    digitalWrite(digitalR, LOW);
    
    digitalWrite(digitalGo, HIGH);
    digitalWrite(digitalWait, LOW);
}
 
void loop() {

    while (Serial1.available() > 0) {
        delay(3);  //delay to allow buffer to fill
          char c = Serial1.read();  //gets one byte from serial buffer
          command += c; //makes the string readString
    }
    
    if(command.length() > 0){
         
        if(command.equals("init")){
            Serial.println("init");
            Serial1.write("OK\n");
        }
        else if(command.equals("b")){
            //Serial.println("baseline");
            Serial1.write("OK\n");

            digitalWrite(digitalGo, LOW);
            digitalWrite(digitalWait, HIGH);

            getDataSet();
            
            digitalWrite(digitalGo, HIGH);
            digitalWrite(digitalWait, LOW);
        }
        else if(command.equals("data")){
            Serial.println("data");
            Serial1.write("OK\n");
        }
        else if(command.equals("reboot")){
            Serial.println("reboot");
            Serial1.write("OK\n");
        }
        else{
            Serial.println(command);
            Serial.println("Invalid command");
            Serial1.write("Invalid\n");
        }
        command = "";
    }
}

void getDataSet(){
  int startTime = millis();
  int currentTime = startTime;

  //get du data pendant 10seconde
  while (currentTime - startTime < 3000){
    digitalWrite(digitalIR, LOW);
    digitalWrite(digitalR, LOW);
    sendData("B", startTime);
  
    digitalWrite(digitalR, HIGH);
    sendData("R", startTime);
  
    digitalWrite(digitalR, LOW);
    sendData("B", startTime);
    
    digitalWrite(digitalIR, HIGH);
    sendData("I", startTime);

    currentTime = millis();
  }

  Serial1.write("END\n");

  
}

void sendData(String pType, int pStartTime){
  val = 0;

  //filtre a moyenne mobile de 500
  for (int i = 0; i <= 500; i++) {
    val += analogRead(analogPin);
  }
  val = val/500;
  timeStamp = millis() - pStartTime;
  String msg = pType + ";" + String(val) + ";" + String(timeStamp) + "\n";
  int l = msg.length();
  //msg = String(l) + "l" + msg;
  char copy[24];
  msg.toCharArray(copy, 24);
  Serial1.write(copy);
  //Serial.print(msg);
}
