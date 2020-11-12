#include <SoftwareSerial.h>
SoftwareSerial myBluetooth(10,11); //RX TX

int analogPin = A3;

String command;
int timeStamp = 0;
int val;
 
void setup() {
    myBluetooth.begin(9600);
    Serial.begin(115200); 
}
 
void loop() {

    while (myBluetooth.available() > 0) {
        delay(3);  //delay to allow buffer to fill
          char c = myBluetooth.read();  //gets one byte from serial buffer
          command += c; //makes the string readString
    }
    
    if(command.length() > 0){
         
        if(command.equals("init")){
            Serial.println("init");
            myBluetooth.write("OK\n");
        }
        else if(command.equals("b")){
            //Serial.println("baseline");
            val = analogRead(analogPin);
            timeStamp = millis();
            String msg = String(val) + ";" + String(timeStamp) + "\n";
            char copy[10];
            msg.toCharArray(copy, 10);
            myBluetooth.write(copy);
            Serial.print(msg);
        }
        else if(command.equals("data")){
            Serial.println("data");
            myBluetooth.write("OK\n");
        }
        else if(command.equals("reboot")){
            Serial.println("reboot");
            myBluetooth.write("OK\n");
        }
        else{
            Serial.println(command);
            Serial.println("Invalid command");
            myBluetooth.write("Invalid\n");
        }
        command = "";
    }
}
