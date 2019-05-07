#!/usr/bin/python
#import cv2
from sick import SICK

print ("<<<< initing sick")
#sick = SICK("/dev/ttyUSB0")
sicke = SICK('COM5')
while True:
    print (".")
    #if sicke.get_frame():
        #print (sicke.cartesian)
        #cv2.imshow("img", sick.image)
        #cv2.waitKey(5)

