#!/usr/bin/env python
import serial,math, struct,commands
from time import *
import datetime
#from camBus_flir import *
#from threading import Thread
#from mpiBusSnifferClass import *

global busPipe
busPipe =  serial.Serial(
port='COM7',
baudrate=9600,
timeout=0.1,
)

class motor(object):
    def __init__(self):
	self.address = '\x00'
	self.stepInMM = 1/1000
	#self.speedConv = 1/((self.stepInMM/1000)/1.6384)
	
    def move(self,pos):
	pos = pos * 10000
	if pos < 0:
		pos = 256^4+pos
	tempWrite = '\x00' + chr(20) + struct.pack('<l',pos)
	busPipe.write(tempWrite)
	busPipe.flush()
	sleep(0.1)
	res = busPipe.read(busPipe.inWaiting())
	print res.encode('hex')

    def position(self):
	tempWrite = '\x00' + chr(60) + struct.pack('<l',0)
	busPipe.write(tempWrite)
	busPipe.flush()
	sleep(0.1)
	res = busPipe.read(busPipe.inWaiting())
	print res.encode('hex')
	pos = struct.unpack('<l',res[2:6])
	print pos[0]
	return pos[0]
	
    def speed(self,spd):
	spd = spd# * self.speedConv
	tempWrite = '\x00' + chr(42) + struct.pack('<l',spd)
	busPipe.write(tempWrite)
	busPipe.flush()
	sleep(0.1)
	res = busPipe.read(busPipe.inWaiting())
	print res.encode('hex')
	






		
