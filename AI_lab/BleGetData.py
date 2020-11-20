import serial
import serial.tools.list_ports
import time
import csv

print("start")

selection = input("> ")
port = "COM4"

bluetooth = serial.Serial(port, 9600)

print("Connected")

bluetooth.flushInput()

print("Get Data")
bluetooth.write(b"init")
input_data = bluetooth.readline()
print(input_data)

selection = input("> Enter Data Name ")
print("Get Data")
bluetooth.write(b"b")
input_data = bluetooth.readline()
print(input_data)

data = "TAG;Value;Time"
dataSet = [data]

while data != "END\n":
    input_data = bluetooth.readline()
    data = input_data.decode("utf-8")
    #print(data.rstrip())
    if data != "END\n":
        dataSet.append(data.rstrip())

print(*dataSet, sep = "\n")

with open(selection  + ".csv", 'w', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(dataSet)