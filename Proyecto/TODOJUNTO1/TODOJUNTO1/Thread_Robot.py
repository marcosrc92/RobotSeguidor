import threading
import time

class Thread_Robot (threading.Thread):  

    def __init__ (self,robot):
        threading.Thread.__init__(self)
        self.robot = robot
        self.etat = True
        self.connexion = True
        
    def run(self): # code exécuté en parallele du programme principal

        while self.connexion: # tant que la connexion n'est pas interompue
            
            time.sleep(0.25)
            ordre = self.robot.arduino.readline().decode('utf-8').strip('\r\n')
        
            if ordre == "STOP" and self.etat:
                self.robot.stop_Moteurs() # on arrête les moteurs
                print("COMMANDE: " + ordre)

            if ordre == "STOP OBSTACLE"  : 
                self.robot.stop_Moteurs() # on arrête les moteurs
                print("DISTANCE INSUFFISANTE, APPUYER SUR LE JOYSTICK POUR DEMI-TOUR")

            if ordre == "FIN CONNEXION": 
                self.connexion = False 
                self.robot.fin_Connexion_Arduino() # arrêt de la connexion à la carte Arduino
                self.robot.fin_Connexion_Kangaroo() # arrêt de la connexion au module Kangaroo x2             
                            
                
