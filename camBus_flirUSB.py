#!/usr/bin/env python
import sys
import PyCapture2
import os
from PIL import Image
from time import *
import numpy, datetime, struct,scipy.misc
from array import array
import tifffile as tiff

def swapEndian(val):
	return struct.unpack("!f", struct.pack(">I", val))[0] 

def dateStr(str):
    print strftime("%Y-%m-%d-%H:%M:%S: "), str

class camera(object):
    def __init__(self):
        self.bus = PyCapture2.BusManager()
        self.numCams = self.bus.getNumOfCameras()
        #self._format = 'RGB'
        trys = 0
        while self.numCams < 1:
            dateStr("Insufficient number of cameras. Try again...")
            trys = trys+1
            sleep(1)
            if trys == 10:
                self.numCams = 2
                dateStr("Not enough cameras. Error expected")

        self.c = PyCapture2.Camera()
        uid = self.bus.getCameraFromIndex(0)
        self.c.connect(uid)
        self.printCameraInfo()
        self.init = 1
        self.ip = "USB"
        self.connErr = 0
        #self.shutterAdj(1)
	

    def printCameraInfo(self):
        camInfo = self.c.getCameraInfo()
        print "Serial number - ", camInfo.serialNumber
        print "Camera model - ", camInfo.modelName
        print "Camera vendor - ", camInfo.vendorName
        print "Sensor - ", camInfo.sensorInfo
        print "Resolution - ", camInfo.sensorResolution
        print "Firmware version - ", camInfo.firmwareVersion
        print "Firmware build time - ", camInfo.firmwareBuildTime

    def start(self):
        if self.connErr:
            dateStr("Camera not connected.")
            exit()
        #print self.c.getNumStreamChannels()
        #stream = self.c.getGigEStreamChannelInfo(self.c.getNumStreamChannels())
        #print dir(stream)

        #imgSetInfo = self.c.Format7ImageSettingsInfo()
        #imgSet = PyCapture2.GigEImageSettings()
        #Image height: 1288
        #Image Width:  964
        self._imageHeight = 1288;
        self._imageWidth = 964;
        #imgSet.offsetX = 0
        #imgSet.offsetY = 0
        #imgSet.height = self._imageHeight
        #imgSet.width = self._imageWidth

       
        #if int(self.ip) == 22:
        #    imgSet.pixelFormat = PyCapture2.PIXEL_FORMAT.MONO8
        #    self._dim = 1
        #else:
        #    imgSet.pixelFormat = PyCapture2.PIXEL_FORMAT.RGB8
        #    self._dim = 3
			
        #print imgSetInfo.__dict__

        #self.c.setGigEImageSettings(imgSet)
        # Start the camera
        self.c.startCapture()

    def stop(self):
        if self.init:
            self.c.stopCapture()


    def bufferExtract(self):
        fc2Ok = 1;
        while fc2Ok:
            try:
                self.image = self.c.retrieveBuffer()
                #print self.c.__dict__
                #dateStr("Taking image")
                fc2Ok = 0
            except PyCapture2.Fc2error as fc2Er:
                dateStr("Error retrieving buffer: "+ self.ip)
                fc2Ok = 1
                continue

    def snap(self,outputimage):
        if self.init:
            self.bufferExtract()
            dateStr("Taking image (" + self.ip + ") : " + outputimage)
            outputimageRAW = self.image.convert(PyCapture2.PIXEL_FORMAT.RGB)
            outputimageRAW.save(outputimage, PyCapture2.IMAGE_FILE_FORMAT.PNG)

    def readReg(self,register):
        return self.c.readRegister(register)

    def writeReg(self,register,val):
        return self.c.writeRegister(register,val)

    def readStreamGigE(self):
        regVal = self.c.readGVCPRegister(0x0D04)
        return regVal

    def writeStreamGigE(self):
        self.c.writeGVCPRegister(0x0D04,9000)
        dateStr("Set GigE file stream to maximum package size:" + self.ip)

    def pixelFormat(self):
        regVal = self.readReg(0x14)
        regVal = regVal*4-0xF00000;
            #newval = struct.unpack(">I", struct.pack("!f", newval))[0] 
        return regVal

    def shutterAdj(self,percent):
        # Handling for registers see doc "Register Reference"
        regVal = self.readReg(0x71C)
        regVal = regVal*4-0xF00000;
        self.minShutter = swapEndian(self.readReg(regVal))
        self.maxShutter = swapEndian(self.readReg(regVal+0x4))
        self.curShutter = swapEndian(self.readReg(regVal+0x8))
        #print self.curShutter
        newval = (self.maxShutter-self.minShutter)*percent+self.minShutter
        #print newval
        dateStr('Update shutter time to ' + str(round(newval*1000)) + 'ms: ' + self.ip)
        newval = struct.unpack(">I", struct.pack("!f", newval))[0] 
        self.writeReg(regVal+0x8,newval)


    def shot(self,outputfolder,outputimage,n):
        if self.init:
            # Averages image if n\ > 1
            self.start()
            self.bufferExtract()
            temp = self.image.getData()
            matrix = numpy.asarray(temp)
            #print dir(self.image)
            #matrixRaw = temp
            i = 0

            temp = self.image.getData()
            matrix = temp

            self.stop()

            out = matrix.view(numpy.uint16).reshape(self._imageWidth,self._imageHeight)


            try:
                #dateStr("Folder for saving images does not exist.")
                print outputfolder
                tiff.imsave(outputfolder+outputimage, out)
            except:
            	dateStr("Folder for saving images does not exist.")
                os.mkdir(outputfolder)
                tiff.imsave(outputfolder+outputimage, out)
                
        else:
            dateStr("Camera not found, therefore it will be skiped: " + self.ip)


        dateStr("Averaging images and saving as: " + outputimage)
