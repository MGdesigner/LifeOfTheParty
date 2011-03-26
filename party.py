import serial
import time
import os

ser=serial.Serial('/dev/ttyUSB0',115200)
tAVG=0
hAVG=0
cAVG=0

for count in range(10):
	ser.write('t')
	ser.read(3)
	b=ser.read()
	a=ser.read()
	temp=(((ord(a)<<8))*0.018)+32
	temp=temp
	ser.read()
	ser.write('f')
	ser.read(5)
	time.sleep(.2)
	ser.write('r')
	ser.read(4)
	a=ser.read()
	relHumid=(ord(a)<<8)/100
	ser.read()
	ser.write('d')
	ser.read(5)
	time.sleep(.2)
	ser.write('c')
	cohtwo=0
	ser.read(4)
	#for i in range(2):
	tmp=ser.read()
	cohtwo= ord(tmp)<<8	
	ser.read()
	ser.write('e')
	ser.read(5)
	time.sleep(.2)
	tAVG+=temp
	hAVG+=relHumid
	cAVG+=cohtwo
tAVG=tAVG/10
hAVG=hAVG/10
cAVG=cAVG/10
print tAVG
print hAVG
print cAVG

