import sys
import time

sys.path.append("C:\\Users\\marco\\OneDrive\\Documentos\\MAIIND\\Robotica\\Proyecto\\TODOJUNTO1\\TODOJUNTO1")
from Thread_Robot import *
sys.path.append("C:\\Users\\marco\\OneDrive\\Documentos\\MAIIND\\Robotica\\Proyecto\\TODOJUNTO1\\TODOJUNTO1")
from classRobot_Arduino import *

robot=Robot_Arduino('COM5','COM10') # creéation du robot
robot.initialisation_Kangaroo() # initialisation du robot
robot.initialisation_Arduino()

thread = Thread_Robot(robot) # création du thread
thread.start() # lancemement du thread

while thread.connexion: # tant que la connexion n'est pas interompue

    time.sleep(0.25)
    
    if thread.etat and thread.connexion: # bloque les ordres si demi-tour en cours

        ordre = robot.arduino.readline().decode('utf-8').strip('\r\n')
        
        if ordre == "AVANCE":
            print("ORDRE: " + ordre)
            robot.vitesse_LigneDroite(0.5,0.25)
            
        if ordre == "RECULE":
            print("ORDRE: " + ordre)
            robot.vitesse_LigneDroite(-0.5,0.25)
            
        if ordre == "DROITE":
            print(" COMMANDE: " + ordre)
            robot.vitesse_Virage(45,0.25)
            
        if ordre == "GAUCHE":
            print("ORDRE: " + ordre)
            robot.vitesse_Virage(-45,0.25)

        if ordre == "DEMI-TOUR":         
            thread.etat = False
            print("ORDRE: " + ordre)              
            #self.robot.demiTour()
            thread.etat=True
            
        print("SpeedDrive " + getSpeedDrive(self))
        print("SpeedTurn " + getSpeedTurn(self))