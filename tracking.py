'''
UNIVERSIDAD DE SAN CARLOS DE GUATEMALA --- ESCUELA DE INGENIERIA MECANICA ELECTRICA--- LABORATORIOS DE ELECTRONICA ---
TRACKING DE FIGURAS GEOMETRICAS ---- PROYECTO ELECTRONICA 6 ----- PRIMER SEMESTRE DEL 2020 ---


--- GRUPO E6_A07 ---
Mario David Garcia Chinchilla 201602882
Edwing Estuardo Alvarez Hernández 201602956
Jefry Carlos Antonio Gonzalez Alay 201612145 	

__________________________________________________________________________________________________________________'''


#Librerias OpenCv, Numpy, Serial, Math, tkinter,sys
import cv2
import numpy as np
import serial
import math
from tkinter import messagebox, simpledialog                       
import sys

bpuerto = False                                         #Bandera para determinar si se encontro el puerto COM

#SE BUSCA EL PUERTO COM DEL DISPOSITIVO Y SE CONECTA AL MISMO.

for iPuerto in range(0, 10):                            #Bulce para recorrer los puertos 
    try:                                                #Excepcion si no se encuentra el puerto
        puerto = 'COM' + str(iPuerto)                   #Se prueba el puerto
        baudios = '115200'                              #Velocidad de transmision 
        ser = serial.Serial(puerto, baudios)         	#Se abre el puerto    
        ser.close()                                  	#Se cierra el puerto
        bpuerto  = True                                 #Se cambia la variable a true, indicando que se encontro el puerto
        break
    except:
        pass

if bpuerto :
    ser = serial.Serial(puerto, baudios)                                            #Se conecta al puerto 
    print('Comunicacion establecida con el puerto: COM ' + str(iPuerto))            #Mensaje de comunicacion establecida en un label
else:
    print('No se ha encontrado el dispositivo')                                                       
    messagebox.showerror("Error", "No se ha encontrado el dispositivo")             #Mensage box de error de comunicacion
    sys.exit()                                                                      #Cerrar el programa


font = cv2.FONT_HERSHEY_SIMPLEX														#Se carga una fuente para los textos.
cap = cv2.VideoCapture(0)															#Se inicia la camara.

#SE DEFINEN LOS COLORES QUE SE DESEAN DETECTAR
azulBajo = np.array([78,158,124],np.uint8)
azulAlto = np.array([138,255,255],np.uint8)

mBajo = np.array([140,100,100],np.uint8)
mAlto = np.array([179,255,255],np.uint8)

amarilloBajo = np.array([15, 52, 72],np.uint8)
amarilloAlto = np.array([102, 255, 255],np.uint8)

#METODO QUE DIBUJA LAS FIGURAS EN PANTALLA

def dibujar(mask,color):
  (cnts, _) = cv2.findContours(mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)							#Se buscan los contornos
  cv2.rectangle(frame,(40,90),(590,380),(255,0,0),3)													#Se establece el area para la deteccion de figuras
  cv2.putText(frame,'Laboratorio de electronica 6',(40,80), font, 0.5,(255,255,255),2,cv2.LINE_AA)		#Se escribe informacion en pantalla
  for c in cnts:																					    
      area = cv2.contourArea(c)																			#Se obtiene el area del contorno
      if area > 3000:
        M = cv2.moments(c)																			    #Se obtienen los momentos del contorno
        if (M["m00"]==0): M["m00"]=1																    #Se busca el centro del contorno
        x = int(M["m10"]/M["m00"])																	    #Se obtiene la coordenada x del centro del contorno
        y = int(M['m01']/M['m00'])																	    #Se obtiene la coordenada y del centro del contorno
        nuevoContorno = cv2.convexHull(c)																#Se suavizan los contornos
        cv2.circle(frame,(x,y),7,(0,255,0),-1)															#Se dibuja un circuto en el centro del contorno
        cv2.putText(frame,'{},{}'.format(x-40,y-90),(x-20,y), font, 0.75,(0,255,0),1,cv2.LINE_AA)		#Se imprimen las coordenadas del centro del contorno
        cv2.drawContours(frame, [nuevoContorno], 0, color, 3)										    #Se dibuja el contorno

        epsilon = 0.01*cv2.arcLength(c,True)															#Se obtienen los vertices del contorno
        approx = cv2.approxPolyDP(c,epsilon,True)
        x2,y2,w,h = cv2.boundingRect(approx)

        if str(color) == "(255, 0, 255)" and len(approx)>10:											#Si el color es magenta y es un circulo
          cv2.putText(frame,'Circulo', (x,y-20),1,1.5,(0,255,0),2)									    #Se imprime que es un circulo
          cx = str(x)																					#Se convierte a string
          cy = str(y)																				    #Se convierte a string
          ccx = "".join([x for x in cx if x.isdigit()]) 												#Se elimina cualquier caracter que no sea un numero
          ccy = "".join([x for x in cy if x.isdigit()]) 												#Se elimina cualquier caracter que no sea un numero
          cadena = "A," + ccx + "," + ccy + '\n'													    #Se crea una caden con el tipo de figura y las coordenadas
          ser.write(cadena.encode("ascii"))																#Se envian las coordendas del centro del circulo
          print(cadena)


        if str(color) == "(255, 0, 255)" and len(approx)==4:											#Si el color es magenta y es un rectangulo
          aspect_ratio = float(w)/h
          if aspect_ratio != 1:
             cv2.putText(frame,'Rectangulo', (x,y-5),1,1.5,(0,255,0),2)									#Se imprime que es un rectangulo
             cx = str(x)																				#Se convierte a string
             cy = str(y)																				#Se convierte a string
             ccx = "".join([x for x in cx if x.isdigit()]) 												#Se elimina cualquier caracter que no sea un numero
             ccy = "".join([x for x in cy if x.isdigit()]) 												#Se elimina cualquier caracter que no sea un numero
             cadena = "R," + ccx + "," + ccy + '\n'													    #Se crea una cadena con el tipo de figura y las coordenadas
             ser.write(cadena.encode("ascii"))															#Se envian las coordendas del centro del rectangulo
             print(cadena)
        

        if str(color) == "(0, 255, 0)" and len(approx)<10:												#Si el color es verde y es un triangulo
          cv2.putText(frame,'Triangulo', (x,y-20),1,1.5,(0,255,0),2)									#Se imprime que es un triangulo
          area = cv2.arcLength(c,True)																	#Se obtiene el area del contorno
          if area > 1200:																				#Se establece un rango de area
            ar = 0;
          elif area < 350:
            ar = 0;
          else:
            ar=0.22*area - 77																			

          cx = str(x)																					#Se convierte a string
          cy = str(y)																					#Se convierte a string
          ccx = "".join([x for x in cx if x.isdigit()]) 												#Se elimina cualquier caracter que no sea un numero
          ccy = "".join([x for x in cy if x.isdigit()]) 												#Se elimina cualquier caracter que no sea un numero
          a = str(int(ar))																				#Se convierte a string
          aar = "".join([x for x in a if x.isdigit()]) 													#Se elimina cualquier caracter que no sea un numero
          cadena = "B," + ccx + "," + ccy + "," + aar + '\n' 											#Se crea una cadena con el tipo de figura, las coordenadas y el area de la fugura
          ser.write(cadena.encode("ascii"))																#Se envia la cadena
          print(cadena)

while True:
  ret,frame = cap.read()
  if ret==True:
    frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    maskAmarillo = cv2.inRange(frameHSV,amarilloBajo,amarilloAlto)
    maskMagenta = cv2.inRange(frameHSV,mBajo,mAlto)
    dibujar(maskAmarillo,(0,255,0))
    dibujar(maskMagenta,(255,0,255))
    cv2.imshow('frame',frame)



    tecla = cv2.waitKey(5) & 0xFF																	  #Si se preciona la tecla ESC se cierra el programa
    if tecla == 27:
      break
cap.release()

cv2.destroyAllWindows()