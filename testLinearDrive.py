#!/usr/bin/env python
import serial,math, struct,commands
from time import *
import datetime
#from camBus_flir import *
from serialLinearDrive import *

#hyper = camera(22)
pos = 0 # End Pos in mm
speed = 1000  # in mm / s
n = 10

linDrive = motor()
linDrive.speed(speed)
#linDrive.move(pos)

#outputfolder = './exp2/';


print "Estimated time (s): " + str(pos / speed)
linDrive.move(pos)
actPos = linDrive.position()

while 1:
    actPos = linDrive.position()
    print actPos
#	outputimage = str(actPos) + '.png'
#	hyper.shot(outputfolder,outputimage,n)
#	print "Position (rel): " + str(actPos / pos / 10000)

linDrive.speed(10000)
linDrive.move(0)






		
