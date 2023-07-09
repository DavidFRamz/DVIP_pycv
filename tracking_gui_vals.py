# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 17:52:55 2017

@author: Me. When i was a Telecommunications and Electronics Engineering student.
"""

import cv2
import numpy as np
import math
from matplotlib import pyplot as plt

video = cv2.VideoCapture('videos/GOPR0649.MP4')
ejex_rojo=[]
ejex_azul =[]
ejey_rojo=[]
ejey_azul =[]
angulo=[]
fps = video.get(5)

kernel = np.ones((3,3),np.uint8)
ret,frame = video.read()

""" First of all is to fix the min and max values of hue, saturation and value, taking account the 
first frame only, in order to track down the red and blue balls along the video."""


# Colors selection GUI

def nothing(x):
   pass

cv2.namedWindow('Blue')
cv2.resizeWindow('Blue',500,300)
cv2.createTrackbar('Hue Min','Blue',0,255,nothing)
cv2.createTrackbar('Hue Max','Blue',0,255,nothing)
cv2.createTrackbar('Saturation Min','Blue',0,255,nothing)
cv2.createTrackbar('Saturation Max','Blue',0,255,nothing)
cv2.createTrackbar('Value Min','Blue',0,255,nothing)
cv2.createTrackbar('Value Max','Blue',0,255,nothing)


while(1):

  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Convert colors space

  #get color range frome gui
  hMin_A = cv2.getTrackbarPos('Hue Min','Blue')
  hMax_A = cv2.getTrackbarPos('Hue Max','Blue')
  sMin_A = cv2.getTrackbarPos('Saturation Min','Blue')
  sMax_A = cv2.getTrackbarPos('Saturation Max','Blue')
  vMin_A = cv2.getTrackbarPos('Value Min','Blue')
  vMax_A = cv2.getTrackbarPos('Value Max','Blue')
  
  

  lower_A=np.array([hMin_A,sMin_A,vMin_A])
  upper_A=np.array([hMax_A,sMax_A,vMax_A])

  #Color detection/ create a blue-mask
  maskcolores_A = cv2.inRange(hsv, lower_A, upper_A)

  #Show mask
  cv2.imshow('frame',frame)
  cv2.imshow('mask',maskcolores_A)
  k = cv2.waitKey(5) & 0xFF
  if k == 27:
    break
cv2.destroyAllWindows()


cv2.namedWindow('Red')
cv2.resizeWindow('Red',500,300)
cv2.createTrackbar('Hue Min','Red',0,255,nothing)
cv2.createTrackbar('Hue Max','Red',0,255,nothing)
cv2.createTrackbar('Saturation Min','Red',0,255,nothing)
cv2.createTrackbar('Saturation Max','Red',0,255,nothing)
cv2.createTrackbar('Value Min','Red',0,255,nothing)
cv2.createTrackbar('Value Max','Red',0,255,nothing)

while(1):
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Convert colors space

  #Get color range from gui
  hMin_R = cv2.getTrackbarPos('Hue Min','Red')
  hMax_R = cv2.getTrackbarPos('Hue Max','Red')
  sMin_R = cv2.getTrackbarPos('Saturation Min','Red')
  sMax_R = cv2.getTrackbarPos('Saturation Max','Red')
  vMin_R = cv2.getTrackbarPos('Value Min','Red')
  vMax_R = cv2.getTrackbarPos('Value Max','Red')
  
  
  lower_R=np.array([hMin_R,sMin_R,vMin_R])
  upper_R=np.array([hMax_R,sMax_R,vMax_R])

  #Color detection/ create a red-mask
  maskcolores_R = cv2.inRange(hsv, lower_R, upper_R)

  #Show mask
  cv2.imshow('frame',frame)
  cv2.imshow('mask',maskcolores_R)
  k = cv2.waitKey(5) & 0xFF
  if k == 27:
    break
cv2.destroyAllWindows()

"""Once the mask parameters have been set and the filtering has been done, we proceed to eliminate
all those small areas that do not correspond to the ball that appear within the declared hsv range
and that are therefore noise for our analysis; for this we use a morphologyEx function which dilates
and compresses the areas where there are bits in 1 in such a way that when the image is restored to
its original shape all the small areas of pixels that do not have an appropriate size with that of 
the balls are eliminated. After this we detect contours and we are left with the largest of them
(which will be where the blue or red ball is) for with this, through the method of moments, detect
the center of the objects that we are going to see and study their behavior in granular media.
 Knowing the position of the red and blue balls we can define a specific area to which to carry 
 out the entire detection procedure (the so-called roi)
"""

########### Eliminating noise and finding contours ###################################
mayorB=0
mayorR=0


openingB = cv2.morphologyEx(maskcolores_A, cv2.MORPH_OPEN, kernel)
openingR = cv2.morphologyEx(maskcolores_R, cv2.MORPH_OPEN, kernel)
contornoB= cv2.findContours(openingB,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]
contornoR= cv2.findContours(openingR,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]
print(len(contornoB))

######################### Find largest contour #####################
for i,j in enumerate(contornoB):
    area = cv2.contourArea(contornoB[i])
    if area>=mayorB:
        mayorB = area
        cntB = j
(x,y),radius = cv2.minEnclosingCircle(cntB)
radio=4*int(radius)
r=int(y)
c=int(x)



for i,j in enumerate(contornoR):
    area=cv2.contourArea(contornoR[i])
    if area>=mayorR:
        mayorR=area
        cntR=j
(x,y),radiusr = cv2.minEnclosingCircle(cntR)
radio_R=4*int(radiusr)
r_R=int(y)
c_R=int(x)


centro=(c,r)
vector_radio=[]
d=math.sqrt((c-c_R)**2+(r-r_R)**2)  #distance  between the blue and red balls
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


############# Processing Video ###########################################
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
         
         
         for i,j in enumerate(contornoB):
            area = cv2.contourArea(contornoB[i])
            if area>=mayorB:
                mayorB = area
                cntB = j

         for i,j in enumerate(contornoR):
            area=cv2.contourArea(contornoR[i])
            if area>=mayorR:
                mayorR=area
                cntR=j

                
                 
         
         #red encircle    
         (x,y),rad = cv2.minEnclosingCircle(cntR)
         center = (int(x)+roi_col,int(y)+roi_fila)
         cR=cv2.circle(frame,center,int(radius),(0,0,255),-2)

         #blue encircle 
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
         
         #angle
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
         
             
             
# Find turning angle
ang_ini=angulo[0]+10
ang_final=0
l=0
while l < len(angulo):
    
    if angulo[l]>=ang_ini:
        ang_final=angulo[l]
    
    l=l+1    
ang_giro=abs(ang_final-ang_ini)         
print("The turning angle is: " + str(ang_giro))   


#==============================================================================
#Analysis and Results    
#==============================================================================

#===============================
#Angular velocity
#===============================


tiempo_a = []
for i in range(0, len(angulo)):
    valor = i/fps
    tiempo_a.append(valor)  
    

velocidad_ang = np.diff(angulo)/(1/fps)


tiempo_v = []
for i in range(0, len(velocidad_ang)):
    valor = i/fps
    tiempo_v.append(valor)  
#===============================
#Linear velocity 
#===============================
d = math.sqrt((c-c_R)**2+(r-r_R)**2) #radius

velocidad_lineal = velocidad_ang*d 

 
#=====================================================             
#Plotting
#=====================================================



#Angle vs time
#=========================================
plt.figure(0)
plt.plot(tiempo_a,angulo,linewidth = 0.5)
plt.title("Angle")
plt.xlabel('time [s]')
plt.ylabel('degrees')
plt.grid()
#Angular velocity vs time
#====================================================
plt.figure(1)
plt.plot(tiempo_v,velocidad_ang*0.0004,linewidth = 0.5,color = 'r')
plt.title("Angular velocity")
plt.xlabel('time [s]')
plt.ylabel('velovelocity [m/s]')
plt.grid()

#Linear velocity vs time
#====================================================
plt.figure(2)
plt.plot(tiempo_v,velocidad_lineal*0.0004,linewidth = 0.5,color = 'g')
plt.title("Linear velocity")
plt.xlabel('time [s]')
plt.ylabel('velocity [m/s]')
plt.grid()



#Position vs time
#====================================================


tiempo_eje = []
for i in range(0, len(ejex_rojo)):
    valor = i/fps
    tiempo_eje.append(valor)  

    
#Position vs x_axis 
plt.figure(3)
plt.plot([tiempo_eje,tiempo_eje],[ejex_rojo,ejex_azul],linewidth = 0.3,color = 'black')
plt.plot(tiempo_eje,ejex_rojo,'.',color = 'r')
plt.plot(tiempo_eje,ejex_azul,'.',color = 'b')
plt.title("Position vs x axis")
plt.xlabel('time [s]')
plt.ylabel('pixels')


#Position vs y_axis
plt.figure(4)
plt.plot([tiempo_eje,tiempo_eje],[ejey_rojo,ejey_azul],linewidth = 0.3,color = 'black')
plt.plot(tiempo_eje,ejey_rojo,'.',color ='r')
plt.plot(tiempo_eje,ejey_azul,'.',color ='b')
plt.title("Position vs y axis")
plt.xlabel('time [s]')
plt.ylabel('pixels')
        
     
#            
#(x, y) vs time
plt.figure(5)
plt.plot([ejex_rojo,ejex_azul],[ejey_rojo,ejey_azul],linewidth = 0.5,color = 'black')
plt.plot(ejex_rojo,ejey_rojo,'.',color = 'r')
plt.plot(ejex_azul,ejey_azul,'.',color = 'b')
plt.title("Positon ")
plt.xlabel('columns')
plt.ylabel('rows')
plt.axis([0,max(ejex_rojo)+20,max(ejey_azul)+20,150])
  
##################################################################################
# plt.figure(6)
# plt.plot(vector_radio,'m')
# plt.title("Intruder's radius vs time")
# plt.xlabel("time")
# plt.ylabel("radius")


# ejex_rojo_new = []
# ejex_azul_new = []
# l=0
# while l < len(ejex_rojo):
#    v=-(l+1)
#    ejex_rojo_new.append(ejex_rojo[v])
#    ejex_azul_new.append( ejex_azul[v])
#    l=l+1
# plt.figure(7)
# plt.plot([ejex_rojo_new,ejex_azul_new],[ejey_rojo,ejey_azul],linewidth = 0.5,color = 'b')
# plt.plot(ejex_rojo_new,ejey_rojo,'.',color = 'r')
# plt.plot(ejex_azul_new,ejey_azul,'.',color = 'b')
# plt.title("Reflected position with respect to x ")
# plt.xlabel('column')
# plt.ylabel('row')
# plt.show()