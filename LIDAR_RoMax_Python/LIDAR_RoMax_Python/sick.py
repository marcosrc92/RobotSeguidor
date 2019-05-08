#!/usr/bin/python
'''
author: Tobias Weis, 2014, [weis DOT tobi AT googlemail.com]

This module communicates with a SICK PLS 101-312 Laserscanner.
Although the protocol is pretty similar to the LM-200, 
I do not know if this would work.

Usage example:

sick = SICK("/dev/ttyUSB0")
while True:
    if sick.get_frame():
        print sick.cartesian
        cv2.imshow("img", sick.image)
        cv2.waitKey(5)


Calling sick.get_frame will automatically fill sick.cartesian and sick.image:

sick.cartesian contains coordinates in the following format:
    [x-coord (in cm), y-coord (in cm), distance (in cm)]

sick.image is an opencv-color-image showing the distances from the scanner

Stuff that helped me along the way (w/ protocols etc.):
- http://www.cs.cmu.edu/afs/cs/project/lri/Meteorite99/Software/src/hardwareDrivers/sick/sickDrv.c
- http://www.cs.cmu.edu/afs/cs/project/lri/Meteorite99/Software/src/hardwareDrivers/sick/sickDefs.h
- https://github.com/hawesie/sicktoolbox/blob/master/c%2B%2B/drivers/pls/sickpls/SickPLS.hh
'''

import serial
import time
import sys
import math
from CRC16_SICK import CRC16_SICK
#import cv2
import numpy as np

SICK_STX = 0x02
SICK_ACK = 0x06
SICK_NAK = 0x15
SICK_NACK = 0x92
SICK_STATUS = 0x31

MAX_DIST = 400 # cm !

#################################### GENERAL MESSAGE LAYOUT TO SICK:
SICK_START = 0x02 # start of transmission
SICK_DEST = 0x00 # dest adress
# payload-length is two addition bytes, makes total of 4 in the header
# now payload bytes
# checksum bytes (2)
###################################################################


class SICK():
    #def __init__(self, port, debug = False, password="SICK_LMS"):
    def __init__(self, port, debug = False):
        print("iniciando el SICK")
        print("Puerto: ", port)
        self._debug = debug
        #self.password = password
        self.ser = serial.Serial(port, 9600)
        self.ser.baudrate = 9600
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.xonxoff = False
        self.ser.rtscts = False
        print("2")
        self.ser.dsrdtr = False
        self.ser.timeout = .1
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.flush()
        print("3")
        self.crc_calc = CRC16_SICK()
        print("4")
        #self.frame = None
        #self.cartesian = None
        #self.image = None
        
        print("Valor del estatus: '%s'", self.test_status)
        # I use this as start sequence to ensure everything is set
        if not self.test_status():
            print ("Trying with baudrate 9600")
            self.ser.baudrate = 9600# checks for reply and changes baudrate if nec
            if not self.test_status():
                raise(Exception("Can not communicate with SICK. Please check connection, port and baudrate"))
        print("Antes de entrar al reset")
        self.reset() # reset and initilize scanner
        print("Saliendo del reset")
        self.log_in() # login with password
        self.set_9k() # set to 98k
        self.request_scan_mode() # request scanning
        self.set_op_mode() # set op-mode to enable scanning, wtf, dont know why

    def calc_distances(self):
        coords = np.empty((0,3))
        for i in range (0,361):
            sval = (self.frame[i*2+8]<<8 | self.frame[i*2+7]) & 0x1fff
            if sval > MAX_DIST: 
                continue
            x =  sval * math.cos(float(i)/2.0*3.1415/180)
            y = sval * math.sin(float(i)/2.0*3.1415/180)
            coords = np.append(coords, np.array([[x,y,sval]]), axis=0)
        self.cartesian = coords

    #def make_image(self):
    #    img = np.zeros(((MAX_DIST + 50),2*(MAX_DIST + 50),3), np.uint8)
    #    for c in self.cartesian:
    #        cv2.circle(img,(int(c[0] + img.shape[1]/2 ),int(img.shape[0] - 20 - c[1])),2,(0,255*c[2]/MAX_DIST,255-255*c[2]/MAX_DIST),1)
    #        cv2.line(img, (img.shape[1]/2, img.shape[0]-20), (int(c[0] + img.shape[1]/2), int(img.shape[0] - 20 - c[1])), (0,255*c[2]/MAX_DIST, (255 - 255*c[2]/MAX_DIST )) )
    #    self.image = img

    def hexar2str(self, hexar):
        return ''.join([chr(c) for c in hexar])

    def parse_msg(self, msg):
        if self._debug:
            print ("[hex(x) for x in msg]")
        if len(msg) > 0:
            response = 0
            if self._debug:
                print ("Length: %d" % (len(msg)))
                if msg[0] == SICK_STX:
                 try:
                    response = msg[4]
                    if response == 0xb0:
                        if self.crc_calc.calcSICK(self.hexar2str(msg[:-2])) == msg[-2:]:
                            self.frame = msg[:-2]
                            self.calc_distances()
                            #self.make_image()
                        else:
                            print ("CHECKSUM DOES NOT MATCH !")
                    elif response == 0xa0:
                        if self._debug:
                            print ("Acknowledged switch operating mode")
                        response = 0xa0
                 except:
                    #print "Error while parsing STX message"
                    pass
            elif msg[0] == SICK_NACK:
                print ("NACK")
            elif msg[0] == SICK_NAK:
                print ("Telegram invalid !")
            elif msg[0] == SICK_ACK:
                try:
                    msg = msg[1:]
                    response = msg[4]
                    data = msg[5:-2]
                    if response == 0xb2:
                        if data[0] == 0x02:
                            print ("Warning: %s" % hex(data[1]))
                        elif data[0] == 0x01:
                            print ("Info: %s" % hex(data[1]))
                        elif data[0] == 0x00:
                            print ("Nothing Wrong")
                        elif data[0] == 0x03:
                            print ("Error: %s" % hex(data[1]))
                        elif data[0] == 0x04:
                            print ("Fatal Error: %s" % hex(data[1]))
                    elif response == SICK_NACK:
                        print ("NACK Telegram !")
                    elif response == 0xa0:
                        if self._debug:
                            print ("Response to switch operating mode")
                        if data[0] == 0x00:
                            if self._debug:
                                print ("Successfull")
                        elif data[0] == 0x01:
                            print ("Not possible, wrong password")
                        else:
                            print ("Dont know, strange stuff: %s" % (hex(data[0])))
                except:
                    #print "Error while parsing ACK message"
                    pass

            if self._debug:
                print (".")
            return response


    def create_and_send_msg(self, msg_to_send):
        print("Entrado a crear el mensaje")
        self.ser.flush()
        msg = []
        msg.append(SICK_START)
        msg.append(SICK_DEST)
        length = len(msg_to_send)
        msg.append(length & 0x00ff) # split length to Hi and Lo byte
        msg.append(length >> 8)
        for i in msg_to_send:
            msg.append(i)
        crc = self.crc_calc.calcSICK(self.hexar2str(msg))
        msg.append(crc[0])
        msg.append(crc[1])
        #msg = [0x02, 0x00, 0x01, 0x00, 0x10, 0x34, 0x12] #esta es la trama de reset (esta sobreescribiendo lo anterior)
        print("mensaje: '%s'", msg)
        print("Saliendo de crear el mensaje")
        self._debug = True
        if self._debug:
            print ("Message: %s" % (''.join([hex(b)+" " for b in msg])))
        self.ser.write(self.hexar2str(msg).encode())
        print("mensaje: '%s'", msg)


    def request_scan_mode(self):
        print ("----------- REQUESTING SCAN MODE:")
        while True:
            self.create_and_send_msg([0x36, 0x01, 10])

            asw = []
            while self.ser.inWaiting() > 0:
                asw.append(ord(self.ser.read(1)))
            if self.parse_msg(asw) == 0xa0:
                print ("Scan request successfull")
                break
            else:
                time.sleep(.01)

    def set_op_mode(self):
        print ("------------- SETTING OPERATION MODE")
        while True:
            self.create_and_send_msg([0x20, 0x24])
            asw = []
            while self.ser.inWaiting() > 0:
                asw.append(ord(self.ser.read(1)))
            if self.parse_msg(asw) == 0xa0:
                print ("Operation mode changed")
                break
            else:
                time.sleep(.1)


    def test_status(self):
        print("Calculando el status")
        count = 0
        while True:
            print("Dentro del bucle")
            self.create_and_send_msg([SICK_STATUS])
            # ATTENTION !
            # IF WE DO NOT RECEIVE A STATUS MESSAGE,
            # SWITCH BAUDRATE TO HIGHER ONE
            # (FOR EXAMPLE WHEN WE ALREADY SET IT BEFORE,
            # BUT RESTARTED THE PROGRAM)
            count = count + 1
            print("Valor de la cuenta: '%s", count)
            if count == 10:
                print ("No response, baudrate wrong ?!")
                return False
            asw = []
            while self.ser.inWaiting() > 0:
                asw.append(ord(self.ser.read(1)))
            if self.parse_msg(asw) == 0xb1:
                print ("TEST: Status message successfull")
                break
            else:
                time.sleep(.1)
        return True


    def set_9k(self):
        print ("Setting 9.8k baudrate")
        pwd = [ord(c) for c in self.password] #this is the master-password of my scanner
        while True:
            self.create_and_send_msg([0x20, 0x40]+pwd)
            asw = []
            while self.ser.inWaiting() > 0:
                asw.append(ord(self.ser.read(1)))
            if self.parse_msg(asw) == 0xa0:
                print ("Speed set to 9.8k, changing speed of self.serial interface")
                self.ser.baudrate = 9800
                break
            else:
                time.sleep(.1)

    '''def log_in(self):
        print ("Logging in")
        pwd = [ord(c) for c in "LASERFUN"]
        while True:
            self.create_and_send_msg([0x20, 0x00]+ pwd)
            asw = []
            while self.ser.inWaiting() > 0:
                asw.append(ord(self.ser.read(1)))
            if self.parse_msg(asw) == 0xa0:
                print ("logged in")
                break
            else:
                time.sleep(.1)'''
    def reset(self):
        print ("Resetting SICK and initing")
        self.create_and_send_msg([0x10])
        print ("Waiting.")
        time.sleep(6)

    def get_frame(self):
        while True:
            asw = []
            start = False
            while len(asw) < (727 + 5):
                while self.ser.inWaiting() > 0:
                    r = ord(self.ser.read(1))
                    if (r == SICK_STX): # read until start-byte discovered
                        start = True
                    if start == True:
                        asw.append(r)
                time.sleep(.0001)
            if self.parse_msg(asw) == 0xb0:
                return True



