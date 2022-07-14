#!/usr/bin/env python
import serial,math, struct,commands
from time import *
import datetime
from camBus_flirUSB import *

hyper = camera()

hyper.shot('./', 'test.tiff', 5)