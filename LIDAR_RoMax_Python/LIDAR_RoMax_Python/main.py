import sys
import time
import numpy as np


#from classRobot import Robot
from sick import SICK

'''
robot=Robot('COM5') #objeto robot
robot.initialisation_Kangaroo() # inicializacion de robot
'''

print ("<<<< initing sick")
sick = SICK('COM1')

asw=sick.get_frame() 
mapa_inicial=sick.calc_distances(asw) #mapa de distancias, no de coordenadas
np_mapa_inicial=np.array(mapa_inicial)
print(np_mapa_inicial[:,2])
print("Sistema en condiciones iniciales, esperando 6 segundos")
time.sleep(6)


#while True: 
#robot.vitesse_LigneDroite(0.5,0.25)
asw1=sick.get_frame() 
mapa_actual=sick.calc_distances(asw1) #mapa de distancias, no de coordenadas
np_mapa_actual=np.array(mapa_actual)
print(np_mapa_actual[:,2])

np_diferencia=np_mapa_inicial[:,2]-np_mapa_actual[:,2]
print(np_diferencia)

'''
for i in range (0,361):
    mapa_diferencial[i]=mapa_inicial[i]-mapa_actual[i]
    print(mapa_diferencial[i])
    #time.sleep(0.25)
'''    