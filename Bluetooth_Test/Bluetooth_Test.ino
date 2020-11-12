#include <SoftwareSerial.h>
SoftwareSerial myBluetooth(10,11); //RX TX


void setup() {
  myBluetooth.begin(9600);
  Serial.begin(115200);
}

void loop() {
  if(myBluetooth.available()>0){
    char lettre = myBluetooth.read();

    if (lettre != -1){
      Serial.println(lettre);
      myBluetooth.write("OK");
    }
  }

}
