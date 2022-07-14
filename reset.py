#!/usr/bin/env python
import serial,math, struct,commands
from time import *
import datetime
from camBus_flir import *
from serialLinearDrive import *

#hyper = camera(22)
pos = 00000
linDrive = motor()
linDrive.speed(2000)
linDrive.move(pos)

outputfolder = './exp1/';
n = 10
#hyper.shot(outputfolder,'test.png',n)

#sudo sysctl -w net.core.rmem_max=1048576 net.core.rmem_default=1048576
#hyper.shot(outputfolder,'test.png',n)
actPos = 0







		
