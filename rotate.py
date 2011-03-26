import serial
from time import sleep
import sys

ser = serial.Serial('/dev/ttyACM0', 9600)
sleep(6)
ser.write('180')
print ser.readline()
sleep(2)
ser.write('1')
sleep(2)
ser.write('180')
sleep(3)

