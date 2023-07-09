import cv2
#from Ej3 import pixel_counter

def clock():
    return cv2.getTickCount() / cv2.getTickFrequency()

#t0 = clock()
#img = cv2.imread("myimage.png", 0)
#pixels = pixel_counter(img, 120)
#t1 = clock()
#
#dt = t1 -t0
#print("Procesamiento realizado en " + str(dt) + " segundos")
