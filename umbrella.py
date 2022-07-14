#!/usr/bin/env python
import serial,math, struct,commands
from time import *
import datetime
from camBus_flirUSB import *
from serialLinearDrive import *

# Requires the flir (now teledyne) python wrapper

hyper = camera()
pos = 30 # End Pos in mm
speed = 100  # in mm / s
n = 20

linDrive = motor()
linDrive.speed(speed)
linDrive.move(pos)

outputfolder = './testExp1/';

actPos = 0

print "Estimated time (s): " + str(pos / speed)

linDrive.position()

while actPos < pos*10000:
	actPos = linDrive.position()
	outputimage = str(actPos) + '.tiff'
	hyper.shot(outputfolder,outputimage,n)
	print "Position (rel): " + str(actPos / pos / 10000 * 100)
	
linDrive.speed(1000)
linDrive.move(0)






		
