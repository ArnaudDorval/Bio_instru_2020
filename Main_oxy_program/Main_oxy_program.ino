//#include <SoftwareSerial.h>
//SoftwareSerial myBluetooth(10,11); //RX TX

int analogPin = A0;

int digitalIR = 50;
int digitalR = 52;

String command;
int timeStamp = 0;
int val;
 
void setup() {
    Serial1.begin(9600);
    Serial.begin(115200); 
    analogReadResolution(16);
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
            val = 0;
            for (int i = 0; i <= 5; i++) {
              val += analogRead(analogPin);
            }
            val = val/5;
            timeStamp = millis();
            String msg = String(val) + ";" + String(timeStamp) + "\n";
            int l = msg.length();
            //msg = String(l) + "l" + msg;
            char copy[15];
            msg.toCharArray(copy, 15);
            Serial1.write(copy);
            Serial.print(msg);
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
