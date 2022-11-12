from typing import Counter
from xmlrpc.client import Server
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import serial
import time

cap = cv2.VideoCapture(1)
detector = HandDetector(maxHands=1)
offset = 20
imgsize = 300
Test_mode = 0 # 0: test without Serial
              # 1: test with Serial 

folder = "Images/3finger" 
counter = 0

if(Test_mode not in [0]):
    arduino = serial.Serial('COM3')
    print(f'connected to {arduino.name}')
    arduino.write("hello".encode())


while True :
    success , img = cap.read()
    hands , img = detector.findHands(img)
    img_white = np.ones((imgsize,imgsize,3),np.uint8)*255
    if hands:
        hand = hands[0]
        try:
            x,y,w,h = hand['bbox']
            imgCrop = img[y-offset:y+h+offset, x-offset:x+w+offset]
            if x < 0:
                x = 0
            if y < 0:
                y = 0
            if h < 1:
                h = 1
            if w < 1:
                w = 1        

            aspectRatio = h/w
            if aspectRatio>1:
                k = imgsize/h
                wCal = math.ceil(k*w)
                imgResize = cv2.resize(imgCrop,(wCal,imgsize))
                widthGap = math.ceil((imgsize - imgResize.shape[1])/2)
                img_white[0:imgResize.shape[0],widthGap:widthGap + imgResize.shape[1]] = imgResize    
            else:
                k = imgsize/w
                hCal = math.ceil(k*h)
                imgResize = cv2.resize(imgCrop,(imgsize,hCal))
                heightGap = math.ceil((imgsize - imgResize.shape[0])/2)
                img_white[heightGap:heightGap+imgResize.shape[0],0:imgResize.shape[1]] = imgResize

            cv2.imshow("Croppedimage" , img_white)








        except Exception as e:
            print(x,y,h,w)
            print(e)
    cv2.imshow("image" , img)
    
    key = cv2.waitKey(1)
    
    if key == ord('s'):
        counter += 1
        print(f'image{counter} saved')
        cv2.imwrite(f'{folder}/Image{time.time()}.jpg', img_white)
    if key == ord('e'):
        break

