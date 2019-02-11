import serial
import time

class Robot_Arduino:
    
    """ La classe définissant un robot caractérisé par :
        - deux ports USB
        - un module Kangaroo x2
        - une carte Arduino
        - une vitesse en ligne droite maximale en m/s
        - une vitesse en virage maximale en °/s """
    
    """ constructeur de la classe Robot_Arduino """
    def __init__(self,port_Kangaroo,port_Arduino):
        self.port_Kangaroo = port_Kangaroo
        self.port_Arduino = port_Arduino
        self.vitesseMax_LigneDroite = 1 #m/s
        self.vitesseMax_Virage = 180 #°/s

    """ méthode pour établir la connexion à la carte Arduino """
    def initialisation_Arduino(self):
        self.arduino=serial.Serial(self.port_Arduino,9600) # établissement de la connexion à la carte Arduino
        print("CONNEXION A L'ARDUINO")
        print("-----------------------------------")
        
    """ méthode pour établir la connexion au Kangaroo x2 et initialiser le contrôle des moteurs """
    def initialisation_Kangaroo(self):
        self.kangaroo = serial.Serial(self.port_Kangaroo,9600) # établissement de la connexion au module Kangaroo x2
        print("CONNEXION AU KANGAROO")
        self.kangaroo.write('D,start\n'.encode('utf-8')) # initialisation des voies D et T
        self.kangaroo.write('T,start\n'.encode('utf-8'))
        self.kangaroo.write('D,s0\n'.encode('utf-8')) # commande de vitesse de 0 m/s obligatoire
        self.kangaroo.write('T,s0\n'.encode('utf-8'))

        
    """ méthode pour faire avancer/reculer le robot à une vitesse donnée en m/s pendant en temps donné en s """
    def vitesse_LigneDroite(self,vitesse,temps):
        if vitesse > self.vitesseMax_LigneDroite: # comparaison avec la vitesse maximale autorisée
            vitesse = self.vitesseMax_LigneDroite
            print("La vitesse a été limitée")
        elif vitesse < -self.vitesseMax_LigneDroite:
            vitesse = -self.vitesseMax_LigneDroite
            print("La vitesse a été limitée")
        vitesseLPR = int(vitesse*2462.5/0.628) # changement d'unité
        commande = 'D,s'+str(vitesseLPR)+'\n'
        self.kangaroo.write(commande.encode('utf-8')) 
        time.sleep(temps)
    
    """ méthode pour faire tourner le robot à une vitesse donnée en °/s pendant un temps donné en s """
    def vitesse_Virage(self,vitesse,temps):
        if vitesse > self.vitesseMax_Virage: # comparaison avec la vitesse maximale autorisée
            vitesse=self.vitesseMax_Virage
            print("La vitesse a été limitée")
        elif vitesse < -self.vitesseMax_Virage:
            vitesse = -self.vitesseMax_Virage
            print("La vitesse a été limitée")
        vitesseLPR = int(vitesse*5540.625/1414) # changement d'unité
        commande = 'T,s'+str(vitesseLPR)+'\n'
        self.kangaroo.write(commande.encode('utf-8')) 
        time.sleep(temps)

    """ méthode pour faire avancer/reculer le robot d'une distance donnée en m à une vitesse donnée en m/s """
    def position_LigneDroite(self,position,vitesse):
        if vitesse > self.vitesseMax_LigneDroite: # comparaison avec la vitesse maximale autorisée aaaaaaaaaaaaaaaaa
            vitesse = self.vitesseMax_LigneDroite
            print("La vitesse a été limitée")
        elif vitesse < -self.vitesseMax_LigneDroite:
            vitesse = -self.vitesseMax_LigneDroite
            print("La vitesse a été limitée")
        vitesseLPR = int(vitesse*2462.5/0.628) # changement d'unité
        positionLPR = int(position*2462.5/0.628)
        commande = 'D,p'+str(positionLPR)+'s'+str(vitesseLPR)+'\n'
        self.kangaroo.write(commande.encode('utf-8'))
        temps = abs(position/vitesse)
        time.sleep(temps)

    """ méthode pour faire tourner le robot d'un nombre de degrès donné à une vitesse donnée en °/s """
    def position_Virage(self,position,vitesse):
        if vitesse > self.vitesseMax_Virage: # comparaison avec la vitesse maximale autorisée aaaaaaaaaaaaaaaaaaaaaa
            vitesse = self.vitesseMax_Virage
            print("La vitesse a été limitée")
        elif vitesse < -self.vitesseMax_Virage:
            vitesse = -self.vitesseMax_Virage
            print("La vitesse a été limitée")
        positionLPR = int(position*5540.625/1414) # changement d'unité
        vitesseLPR = int(vitesse*5540.625/1414)
        commande = 'T,p'+str(positionLPR)+'s'+str(vitesseLPR)+'\n'
        self.kangaroo.write(commande.encode('utf-8'))
        temps = abs(position/vitesse)
        time.sleep(temps)

    """ méthode pour faire faire au robot un demi-tour """
    def demiTour(self):
        vitesseLPR = int(0.2*2462.5/0.628)
        positionLPR = int(-0.4*2462.5/0.628)
        commande = 'D,p'+str(positionLPR)+'s'+str(vitesseLPR)+'\n'
        self.kangaroo.write(commande.encode('utf-8'))
        temps = abs(0.4/0.2)
        time.sleep(temps+1)
        positionLPR = int(180*5540.625/1414)
        vitesseLPR = int(90*5540.625/1414)
        commande = 'T,p'+str(positionLPR)+'s'+str(vitesseLPR)+'\n'
        self.kangaroo.write(commande.encode('utf-8'))
        temps = abs(180/90)
        time.sleep(temps)

    """ méthode pour stopper les moteurs """
    def stop_Moteurs(self):
        self.kangaroo.write('D,powerdown\n'.encode('utf-8')) # arrêt du contôle des voies D et T
        self.kangaroo.write('T,powerdown\n'.encode('utf-8'))
        self.kangaroo.write('D,start\n'.encode('utf-8')) # initialisation des voies D et T
        self.kangaroo.write('T,start\n'.encode('utf-8'))
        self.kangaroo.write('D,s0\n'.encode('utf-8')) # commande de vitesse de 0 m/s obligatoire
        self.kangaroo.write('T,s0\n'.encode('utf-8'))

    """ méthode pour stopper le contrôle des moteurs et arrêter la connexion au Kangaroo """
    def fin_Connexion_Kangaroo(self):
        if self.kangaroo.isOpen() == True:
            self.kangaroo.write('D,powerdown\n'.encode('utf-8')) # arrêt du contôle des voies D et T
            self.kangaroo.write('T,powerdown\n'.encode('utf-8'))
            self.kangaroo.close() # arrêt de la connexion au module Kangaroo x2
            print("FIN DE LA CONNEXION AU KANGAROO")

    """ méthode pour arrêter la connexion à l'Arduino """
    def fin_Connexion_Arduino(self):
        if self.arduino.isOpen()== True:
            self.arduino.close() # arrêt de la connexion à la carte Arduino
            print("-------------------------------------------")
            print("FIN DE LA CONNEXION A L'ARDUINO")
   
