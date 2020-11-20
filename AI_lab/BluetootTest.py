import serial
import serial.tools.list_ports
import time

print("start")

selection = input("> ")
port = "COM4"

bluetooth = serial.Serial(port, 9600)

print("Connected")

bluetooth.flushInput()

for i in range(5):
    print("Ping")
    bluetooth.write(b"init")
    input_data = bluetooth.readline()
    print(input_data)