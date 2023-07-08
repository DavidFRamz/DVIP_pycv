# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 17:52:55 2017

@author: Yo. Telecommunications and Electronics Engineering student.
"""




import cv2
import numpy as np
import math
from matplotlib import pyplot as plt

video = cv2.VideoCapture('GOPR0649.MP4')
ejex_rojo=[]
ejex_azul =[]
ejey_rojo=[]
ejey_azul =[]
angulo=[]
fps = video.get(5)

kernel = np.ones((3,3),np.uint8)
ret,frame = video.read()

#Lo primero que vamos a hacer es fijar los parametros de hue,value y saturation maximos y minimos segun el primer frame del video
#para encontrar las bolas azul y roja;esto lo hariamos para definir una roi determinada para seguir el rastreo.No le fijamos directamente
#el rango de valores, pues este cambia en cada video por la calidad de imagen en cada uno de ellos.


# Prueba de colores

def nothing(x):
   pass

#Creamos una ventana llamada 'image' en la que habra todos los sliders
cv2.namedWindow('Azul')
cv2.resizeWindow('Azul',500,300)
cv2.createTrackbar('Hue Minimo','Azul',0,255,nothing)
cv2.createTrackbar('Hue Maximo','Azul',0,255,nothing)
cv2.createTrackbar('Saturation Minimo','Azul',0,255,nothing)
cv2.createTrackbar('Saturation Maximo','Azul',0,255,nothing)
cv2.createTrackbar('Value Minimo','Azul',0,255,nothing)
cv2.createTrackbar('Value Maximo','Azul',0,255,nothing)


while(1):
#   _,frame = video.read() #Leer un frame

  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Convertirlo a espacio de color HSV

  #Los valores maximo y minimo de H,S y V se guardan en funcion de la posicion de los sliders
  hMin_A = cv2.getTrackbarPos('Hue Minimo','Azul')
  hMax_A = cv2.getTrackbarPos('Hue Maximo','Azul')
  sMin_A = cv2.getTrackbarPos('Saturation Minimo','Azul')
  sMax_A = cv2.getTrackbarPos('Saturation Maximo','Azul')
  vMin_A = cv2.getTrackbarPos('Value Minimo','Azul')
  vMax_A = cv2.getTrackbarPos('Value Maximo','Azul')
  
  

  #Se crea un array con las posiciones minimas y maximas
  lower_A=np.array([hMin_A,sMin_A,vMin_A])
  upper_A=np.array([hMax_A,sMax_A,vMax_A])

  #Deteccion de colores
  maskcolores_A = cv2.inRange(hsv, lower_A, upper_A)

  #Mostrar los resultados y salir
  cv2.imshow('frame',frame)
  cv2.imshow('mask',maskcolores_A)
  k = cv2.waitKey(5) & 0xFF
  if k == 27:
    break
cv2.destroyAllWindows()
# video.release()




cv2.namedWindow('Rojo')
cv2.resizeWindow('Rojo',500,300)
cv2.createTrackbar('Hue Minimo','Rojo',0,255,nothing)
cv2.createTrackbar('Hue Maximo','Rojo',0,255,nothing)
cv2.createTrackbar('Saturation Minimo','Rojo',0,255,nothing)
cv2.createTrackbar('Saturation Maximo','Rojo',0,255,nothing)
cv2.createTrackbar('Value Minimo','Rojo',0,255,nothing)
cv2.createTrackbar('Value Maximo','Rojo',0,255,nothing)

while(1):

#   _,frame = video.read() #Leer un frame
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Convertirlo a espacio de color HSV

  #Los valores maximo y minimo de H,S y V se guardan en funcion de la posicion de los sliders
  hMin_R = cv2.getTrackbarPos('Hue Minimo','Rojo')
  hMax_R = cv2.getTrackbarPos('Hue Maximo','Rojo')
  sMin_R = cv2.getTrackbarPos('Saturation Minimo','Rojo')
  sMax_R = cv2.getTrackbarPos('Saturation Maximo','Rojo')
  vMin_R = cv2.getTrackbarPos('Value Minimo','Rojo')
  vMax_R = cv2.getTrackbarPos('Value Maximo','Rojo')
  
  

  #Se crea un array con las posiciones minimas y maximas
  lower_R=np.array([hMin_R,sMin_R,vMin_R])
  upper_R=np.array([hMax_R,sMax_R,vMax_R])

  #Deteccion de colores
  maskcolores_R = cv2.inRange(hsv, lower_R, upper_R)

  #Mostrar los resultados y salir
  cv2.imshow('frame',frame)
  cv2.imshow('mask',maskcolores_R)
  k = cv2.waitKey(5) & 0xFF
  if k == 27:
    break
cv2.destroyAllWindows()

#Una vez fijada las parametros de la mascara y realizado el filtrado pasamos a eliminar todas aquellas pequeñas zonas que no corresponden
# a la bola que aparecen dentro del rango de hsv declarado y que por lo tanto son ruido para nuestro analisis;para ello empleamos una 
#funcion morphologyEx la cual dilata y comprime las zonas donde existan bit en 1 de tal forma que cuando se restabece la imagen a su
#forma original todas las pequeñas areas de pixeles que no tienen un tamaño apropiado con el de las bolas queda eliminado.Luego de esto
#detectamos contornos y nos quedamos con el mayor de ellos(que sera donde este la bola azul o roja) para con este a traves del metodo de
#los momentos detectar el centro de los objetos que vamos a ver y estudiar su comportamiento en medios granulares.Conociendo ya la posicion 
# de las bolas roja y azul podemos definir una zona especifica a la cual realizarle todo el procedimiento de deteccion(la llamada roi)


###########eliminando ruido y hallando contorno###################################
mayorB=0
mayorR=0


openingB = cv2.morphologyEx(maskcolores_A, cv2.MORPH_OPEN, kernel)
openingR = cv2.morphologyEx(maskcolores_R, cv2.MORPH_OPEN, kernel)
contornoB= cv2.findContours(openingB,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]
contornoR= cv2.findContours(openingR,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]
print(len(contornoB))
######################### encontrando el mayor contorno #####################
l=0
while l<len(contornoB):
    area=cv2.contourArea(contornoB[l])
    if area>=mayorB:
        mayorB=area
        cntB=contornoB[l]
    l=l+1
(x,y),radius = cv2.minEnclosingCircle(cntB)
radio=4*int(radius)
r=int(y)
c=int(x)

l=0
while l<len(contornoR):
    area=cv2.contourArea(contornoR[l])
    if area>=mayorR:
        mayorR=area
        cntR=contornoR[l]
    l=l+1
(x,y),radiusr = cv2.minEnclosingCircle(cntR)
radio_R=4*int(radiusr)
r_R=int(y)
c_R=int(x)


centro=(c,r)
vector_radio=[]#este vector lo utilizaremos para comprobar que el radio del intruso se mantenga constante en el tiempo
d=math.sqrt((c-c_R)**2+(r-r_R)**2)#distancia a la que se encuentra la bola roja de la azul
vector_radio.append(d)
desplazamiento=int(d)+radio_R

if c_R<c:
    if desplazamiento > c:
        roi_col=abs(c_R-radio_R)
        if roi_col<20:
            roi_col=0
    else:
        roi_col=c-desplazamiento
else:
    if desplazamiento > c:
        roi_col=desplazamiento-c
    else:
        roi_col=c-desplazamiento

    
roi_fila=r-desplazamiento
ancho=2*desplazamiento


############# Metodo mio para cada frame del video ###########################################
while(1):
     ret, frame = video.read()
     
     if ret == True:

         roi =frame[roi_fila:roi_fila+ancho,roi_col:roi_col+ancho]
        
         hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
         
         maskR = cv2.inRange(hsv, lower_R,upper_R)
        
         maskB = cv2.inRange(hsv, lower_A,upper_A)
         
         openingR = cv2.morphologyEx(maskR, cv2.MORPH_OPEN, kernel)
         
         openingB = cv2.morphologyEx(maskB, cv2.MORPH_OPEN, kernel)
         
         contornoR= cv2.findContours(openingR,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]
        
         contornoB= cv2.findContours(openingB,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]
         
         mayorR=0
       
         mayorB=0
         #cogiendo el cnt bola roja
         l=0
         while l<len(contornoB):
            area=cv2.contourArea(contornoB[l])
            if area>=mayorB:
                mayorB=area
                cntB=contornoB[l]
            l=l+1
                 
               
                 
         #azul       
         l=0
         while l<len(contornoR):
            area=cv2.contourArea(contornoR[l])
            if area>=mayorR:
                mayorR=area
                cntR=contornoR[l]
            l=l+1
                 
         
         #circuncirculo rojo      
         (x,y),rad = cv2.minEnclosingCircle(cntR)
         center = (int(x)+roi_col,int(y)+roi_fila)
         cR=cv2.circle(frame,center,int(radius),(0,0,255),-2)

         #circuncirculo  azul 
         (x,y),radi = cv2.minEnclosingCircle(cntB)
         center = (int(x)+roi_col,int(y)+roi_fila)
         cB=cv2.circle(frame,center,int(radiusr),(255,0,0),-2)

                      
                 
         moments1 = cv2.moments(cntR)
    
         moments3 = cv2.moments(cntB)
         
         
         if moments1['m00']!=0:
            x_r = int(moments1['m10']/moments1['m00'])
            y_r = int(moments1['m01']/moments1['m00'])
            x_r = x_r + roi_col
            y_r = y_r + roi_fila
         else:
            x_r=moments1['m00']
            y_r=moments1['m00']
            
         
         ejex_rojo.append(x_r)
         ejey_rojo.append(y_r)
        
         
        
         if moments3['m00']!=0:
            x_a = int(moments3['m10']/moments3['m00'])
            y_a = int(moments3['m01']/moments3['m00'])
            x_a = x_a + roi_col
            y_a = y_a + roi_fila
         else:
            x_a=moments3['m00']
            y_a=moments3['m00']
         
         ejex_azul.append(x_a)
         ejey_azul.append(y_a)
         
         d1=math.sqrt((x_a-x_r)**2+(y_a-y_r)**2)
         vector_radio.append(d1)
         if x_r<x_a:
             if desplazamiento >int( x_a) :
                 roi_col=abs(int(x_r)-radio_R)
                 
             else:
                 roi_col=int(x_a)-desplazamiento
         else:
             if desplazamiento >int( x_a):
                 roi_col=desplazamiento-int(x_a)
             else:
                 roi_col=int(x_a)-desplazamiento
         
         roi_fila=int(y_a)-desplazamiento
         
         #hallando  angulo
         x=x_r-x_a
         y=y_a-y_r
         

         
         var=complex(x,y)
         var=np.angle(var,deg=1)
         angulo.append(var)
                 
         cv2.imshow('frame',frame)
         cv2.imshow('roi',roi)
         cv2.imshow('mask',maskR)
         cv2.imshow('maskb',maskB)

         k = cv2.waitKey(60) & 0xFF
         if k == 27:
            break
     else:
        break
    
cv2.destroyAllWindows()
video.release()
         
             
             
#
#
##Determinar angulo de giro
ang_ini=angulo[0]+10
ang_final=0####no estaba
l=0
while l < len(angulo):
    
    if angulo[l]>=ang_ini:
        ang_final=angulo[l]
    
    l=l+1    
ang_giro=abs(ang_final-ang_ini)         
print("El angulo de giro es:" + str(ang_giro))  
#
##Determinar la velocidad angular   
#velocidad_ang=np.diff(angulo)/(1/119.88) 
#
#
#
#
##Determinar la velocidad lineal
#
#velocidad_lineal=velocidad_ang*d  


                
#==============================================================================
#ANALISIS Y RESULTADOS     
#==============================================================================

#===============================
#DETERMINAR ANGULO DE GIRO
#===============================


#Definir indice de tiempo
ta = range(0, len(angulo))

#Conformar el eje de tiempo para graficar el angulo
tiempo_a = []


for i in ta:
    valor = i/fps
    tiempo_a.append(valor)  
    

velocidad_ang = np.diff(angulo)/(1/fps)

#Definir indice de tiempo
tv = range(0, len(velocidad_ang))

#Conformar el eje de tiempo para graficar la velocidad
tiempo_v = []
for i in tv:
    valor = i/fps
    tiempo_v.append(valor)  


#===============================
#DETERMINAR VELOCIDAD LINEAL 
#===============================
d = math.sqrt((c-c_R)**2+(r-r_R)**2) #Encontrar el radio del circul(distancia e/ azul y rojo)

velocidad_lineal = velocidad_ang*d 

 
#=====================================================             
#REPRESENTACION GRAFICA DE LOS RESULTADOS
#=====================================================



#GRAFICAR EL ANGULO EN FUNCION DEL TIEMPO
#=========================================
plt.figure(0)
plt.plot(tiempo_a,angulo,linewidth = 0.5)
plt.title("ANGULO")
plt.xlabel('tiempo [s]')
plt.ylabel('grado')
plt.grid()
#GRAFICAR LA VELOCIDAD ANGULAR EN FUNCION DEL TIEMPO
#====================================================
plt.figure(1)
plt.plot(tiempo_v,velocidad_ang*0.0004,linewidth = 0.5,color = 'r')
plt.title("VELOCIDAD ANGULAR")
plt.xlabel('tiempo [s]')
plt.ylabel('velocidad [m/s]')
plt.grid()

#GRAFICAR LA VELOCIDAD LINEAL EN FUNCION DEL TIEMPO
#====================================================
plt.figure(2)
plt.plot(tiempo_v,velocidad_lineal*0.0004,linewidth = 0.5,color = 'g')
plt.title("VELOCIDAD LINEAL")
plt.xlabel('tiempo [s]')
plt.ylabel('velocidad [m/s]')
plt.grid()



#GRAFICAR LA POSICIONL EN FUNCION DEL TIEMPO
#====================================================



#Definir indice de tiempo
teje = range(0, len(ejex_rojo))


#Conformar el eje de tiempo para graficar la velocidad
tiempo_eje = []

for i in teje:
    valor = i/fps
    tiempo_eje.append(valor)  

    
#Posicion en x de los circulos azul y rojo  
plt.figure(3)
plt.plot([tiempo_eje,tiempo_eje],[ejex_rojo,ejex_azul],linewidth = 0.3,color = 'black')
plt.plot(tiempo_eje,ejex_rojo,'.',color = 'r')
plt.plot(tiempo_eje,ejex_azul,'.',color = 'b')
plt.title("POSICION EN EL EJE X")
plt.xlabel('tiempo [s]')
plt.ylabel('pixel')


 #Posicion en y de los circulos azul y rojo 
#estas dos ultimas graficas nos salen poniendolas directamente en la consola no corriendo el programa
#eso lo arreglamos despues  
plt.figure(4)
plt.plot([tiempo_eje,tiempo_eje],[ejey_rojo,ejey_azul],linewidth = 0.3,color = 'black')
plt.plot(tiempo_eje,ejey_rojo,'.',color ='r')
plt.plot(tiempo_eje,ejey_azul,'.',color ='b')
plt.title("POSICION EN EL EJE Y")
plt.xlabel('tiempo [s]')
plt.ylabel('pixel')
        
     
#            
#VARIANTE (IV) (ploteo de fila x columna)=> este es el ploteo bueno bueno
plt.figure(5)
plt.plot([ejex_rojo,ejex_azul],[ejey_rojo,ejey_azul],linewidth = 0.5,color = 'black')
plt.plot(ejex_rojo,ejey_rojo,'.',color = 'r')
plt.plot(ejex_azul,ejey_azul,'.',color = 'b')
plt.title("POSICION ")
plt.xlabel('columna')
plt.ylabel('fila')
  
##################################################################################
plt.figure(6)
plt.plot(vector_radio,'m')
plt.title("Radio del intruso en el tiempo ")
plt.xlabel('tiempo')
plt.ylabel('radio')


#Essto es para invertir los valores de la lista y plotear como en el video
ejex_rojo_new = []
ejex_azul_new = []
l=0
while l < len(ejex_rojo):
   v=-(l+1)
   ejex_rojo_new.append(ejex_rojo[v])
   ejex_azul_new.append( ejex_azul[v])
   l=l+1
plt.figure(7)
plt.plot([ejex_rojo_new,ejex_azul_new],[ejey_rojo,ejey_azul],linewidth = 0.5,color = 'b')
plt.plot(ejex_rojo_new,ejey_rojo,'.',color = 'r')
plt.plot(ejex_azul_new,ejey_azul,'.',color = 'b')
plt.title("POSICION refejada en x ")
plt.xlabel('columna')
plt.ylabel('fila')
plt.show()