# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 15:03:23 2019

@author: Portatil Chema
"""

import serial
import time
import sys
import math

class SICK():
    #def __init__(self, port, debug = False, password="SICK_LMS"):
    def __init__(self, port, debug = False):
        print("iniciando el SICK")
        self._debug = debug
        #self.password = password
        self.ser = serial.Serial(port, 9600)
        self.ser.baudrate = 9600
        self.ser.parity = serial.PARITY_ODD
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.xonxoff = True
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
        
        #print("Valor del estatus: '%s'", self.test_status)
        # I use this as start sequence to ensure everything is set
        if not self.test_status():
            print ("Trying with baudrate 9600")
            self.ser.baudrate = 9600# checks for reply and changes baudrate if nec
            if not self.test_status():
                raise(Exception("Can not communicate with SICK. Please check connection, port and baudrate"))
        print("Antes de entrar al reset")
        self.reset() # reset and initilize scanner
        print("Saliendo del reset")