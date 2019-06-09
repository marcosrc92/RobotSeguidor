# RobotSeguidor
Este proyecto está desarrollado por el departamento de robótica de la Universidad de Oviedo.

El proyecto consiste en la detección del movimiento dentro de una zona previamente delimitada, para que un robot de función colaborativa 
sea capaz de realizar el seguimiento de un objetivo previamente fijado(humanos, robots, etc) dentro de las instalaciones. A su vez, se busca 
que en presencia humana el resto de los robots sean capaces de seguir trabajando sin ninguna interferencia a nos ser que alguien 
se interponga dentro del área de seguridad del robot.

Para ello, se realiza un mapeado de la instalacion cada 0.5 segundos para llevar a cabo la detección del movimiento. La información proveniente
del mapa será tratada y analizada para determinar el sentido en el que el objetivo se mueve. Determinada la posición del elemento a seguir,
se transmitirá la información relativa al movimiento que debe realizar el robot. De tal manera que, a mayor distancia, el robot se desplazará
a una velocidad mayor para alcanzar el objetivo. En el caso contrario, si el elemento a seguir se encuentra en una posición cercana, el robot
se desplazará a una velocidad menor.

Lugar de pruebas:        * Laboratorio de robótica de la Universidad de Oviedo.                       
Sensor Laser(LIDAR):     * SICK - LMS200                                        
Robot experimental:      * Movirobotics
