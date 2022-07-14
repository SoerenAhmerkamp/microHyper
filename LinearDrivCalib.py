#!/usr/bin/env python
import serial,math, struct,commands
from time import *
import datetime
#from camBus_flir import *
from serialLinearDrive import *

#hyper = camera(22)
pos = 20 # End Pos in mm
speed = 1000  # in mm / s
n = 10

linDrive = motor()
linDrive.speed(speed)
#linDrive.move(pos)

#outputfolder = './exp2/';


print "Estimated time (s): " + str(pos / speed)
linDrive.move(pos)
actPos = linDrive.position()
forw = 1

while 1:
    actPos = linDrive.position()
    print actPos
    if actPos == pos*10000:
        if forw == 0:
            pos = 20
            forw = 1
            linDrive.move(pos)
        else:
            pos = 0
            forw = 0
            linDrive.move(pos)
#	outputimage = str(actPos) + '.png'
#	hyper.shot(outputfolder,outputimage,n)
#	print "Position (rel): " + str(actPos / pos / 10000)

linDrive.speed(1000)
linDrive.move(0)






		
