import sys
import time
import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt

from classRobot import Robot
from sick import SICK



robot=Robot('COM5') #objeto robot
robot.initialisation_Kangaroo() # inicializacion de robot


print ("<<<< initing sick")
sick = SICK('COM1')

#evita que el programa se detenga al mostrar una figura
plt.show()
plt.interactive=True

print("Primera foto")
asw=sick.get_frame() 
mapa_inicial_1=sick.calc_distances(asw)
np_mapa_inicial_1=np.array(mapa_inicial_1)

time.sleep(0.2)

print("Segunda foto")
asw1=sick.get_frame() 
mapa_inicial_2=sick.calc_distances(asw1)
np_mapa_inicial_2=np.array(mapa_inicial_2)

time.sleep(0.2)

print("Tercera foto")
asw2=sick.get_frame() 
mapa_inicial_3=sick.calc_distances(asw2)
np_mapa_inicial_3=np.array(mapa_inicial_3)

time.sleep(0.2)

print("Cuarta foto")
asw3=sick.get_frame() 
mapa_inicial_4=sick.calc_distances(asw3)
np_mapa_inicial_4=np.array(mapa_inicial_4)

time.sleep(0.2)

print("Quinta foto")
asw4=sick.get_frame() 
mapa_inicial_5=sick.calc_distances(asw4)
np_mapa_inicial_5=np.array(mapa_inicial_5)

time.sleep(0.2)

#Se va a sbreescribir todo sobre esta
asw5=sick.get_frame() 
mapa_inicial_filtrado=sick.calc_distances(asw5)
np_mapa_inicial_filtrado=np.array(mapa_inicial_filtrado)

time.sleep(0.2)

# mediana   
for i in range (0,361):
    l = [mapa_inicial_1[i,2], mapa_inicial_2[i,2], mapa_inicial_3[i,2], mapa_inicial_4[i,2], mapa_inicial_5[i,2]]
    l.sort()                                                                                                                                                             
    mediana=l[2]
    np_mapa_inicial_filtrado[i,2]=mediana
    x =  mediana * math.cos(float(i)/2.0*3.1415/180)
    np_mapa_inicial_filtrado[i,0]=x
    y = mediana * math.sin(float(i)/2.0*3.1415/180)
    np_mapa_inicial_filtrado[i,1]=y

  
fig, ax = plt.subplots()
ax.plot(np_mapa_inicial_filtrado[:,0], np_mapa_inicial_filtrado[:,1])
ax.grid()  
#plt.show()
plt.plot(np_mapa_inicial_filtrado[:,0], np_mapa_inicial_filtrado[:,1])

print("Sistema en condiciones iniciales, esperando 6 segundos")
time.sleep(6)


while True: 
    asw_actual=sick.get_frame() 
    mapa_actual=sick.calc_distances(asw_actual)
    np_mapa_actual=np.array(mapa_actual)

    fig, ax = plt.subplots()
    ax.plot(np_mapa_actual[:,0], np_mapa_actual[:,1])
    #evita que el programa se detenga al mostrar una figura
    plt.interactive=True
    ax.grid()  
    plt.plot(np_mapa_actual[:,0], np_mapa_actual[:,1])

    np_diferencia_x=np_mapa_inicial_filtrado[:,0]-np_mapa_actual[:,0]
    np_diferencia_y=np_mapa_inicial_filtrado[:,1]-np_mapa_actual[:,1]
    np_diferencia_mod=np_mapa_inicial_filtrado[:,2]-np_mapa_actual[:,2]

    fig, ax = plt.subplots()
    ax.plot(np_diferencia_x, np_diferencia_y)
    ax.grid()
    plt.plot(np_diferencia_x, np_diferencia_y)


    #busqueda del objeto
    flag_entrada=0
    flag_salida=0
    angulo_salida=0
    angulo_entrada=0
    for i in range (0,361):
        if (np_diferencia_mod[i]>300 and flag_entrada==0):
            angulo_entrada=float(i)/2.0
            flag_entrada=1
        if (np_diferencia_mod[i]<300 and np_diferencia_mod[i]>0 and flag_entrada==1 and flag_salida==0):
            angulo_salida=float(i)/2.0
            flag_salida=1
        diff=abs(angulo_salida-angulo_entrada)
        if (diff<=10):
            flag_entrada=0
            flag_salida=0

    print (angulo_entrada)
    print (angulo_salida)

    angulo_medio=(angulo_salida+angulo_entrada)/2.0

    if(angulo_medio<45.0):
        robot.vitesse_Virage(45,0.25)
    elif(angulo_medio>=45.0 and angulo_medio<=135.0):
        robot.vitesse_LigneDroite(0.5,0.25)
    elif(angulo_medio>135.0):
        robot.vitesse_Virage(-45,0.25)
    else:
        robot.stop_Moteurs()

    #plt.interactive=True
    #plt.show()
    


'''
polares = np.empty((0,2))
for i in range (0,361):
    polares = np.append(polares, np.array([float(i/2.0), np_diferencia_mod[i]]))
print(polares)

coord_x = np.empty((0,2))
for i in range (0,361):
    coord_x = np.append(coord_x, np.array([float(i/2), np_diferencia_x[i]]))
print(coord_x)

coord_y = np.empty((0,2))
for i in range (0,361):
    coord_y = np.append(coord_y, np.array([float(i/2), np_diferencia_y[i]]))
print(coord_y)
'''

print ("FIN")  