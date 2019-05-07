import sys
import time

import classRobot
import sick
from sick import SICK

robot=Robot('COM5') #objeto robot
robot.initialisation_Kangaroo() # inicializacion de robot

thread = Thread_Robot(robot) # creacion del hilo
thread.start() # lanzamiento del hilo

print ("<<<< initing sick")
sick = SICK('COM5')

while thread.connexion: # tant que la connexion n'est pas interompue
    SICK.get_frame()
    robot.vitesse_LigneDroite(0.5,0.25)
    time.sleep(0.25)
    
    #if thread.etat and thread.connexion: # bloque les ordres si demi-tour en cours

        #ordre = robot.arduino.readline().decode('utf-8').strip('\r\n')
        
        #if ordre == "AVANCE":
            #print("ORDRE: " + ordre)
            #robot.vitesse_LigneDroite(0.5,0.25)
            
        #if ordre == "RECULE":
            #print("ORDRE: " + ordre)
            #robot.vitesse_LigneDroite(-0.5,0.25)
            
        #if ordre == "DROITE":
            #print(" COMMANDE: " + ordre)
            #robot.vitesse_Virage(45,0.25)
            
        #if ordre == "GAUCHE":
            #print("ORDRE: " + ordre)
            #robot.vitesse_Virage(-45,0.25)

        #if ordre == "DEMI-TOUR":         
            #thread.etat = False
            #print("ORDRE: " + ordre)              
            ##self.robot.demiTour()
            #thread.etat=True