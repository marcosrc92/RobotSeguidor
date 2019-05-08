import sys
import time

#import Conexion_Sick
from classRobot import Robot
from sick import SICK


robot=Robot('COM5') #objeto robot
robot.initialisation_Kangaroo() # inicializacion de robot

print ("<<<< initing sick")
sick = SICK('COM1')

while True: 
    robot.vitesse_LigneDroite(0.5,0.25)
    time.sleep(0.25)
    