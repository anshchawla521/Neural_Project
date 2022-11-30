
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import serial
import time

cap = cv2.VideoCapture(1)
detector = HandDetector(maxHands=1)
classifier = Classifier("model/keras_model.h5","model/labels.txt")
offset = 20
imgsize = 300
Test_mode = 1 # 0: test without Serial
              # 1: test with Serial 

folder = "Images/C" 
counter = 0
labels = []
with open("model/labels.txt") as file:
    for line in file:
        labels.append(line.strip().split()[1])
    #print(labels)




if(Test_mode not in [0]):
    arduino = serial.Serial('COM6',baudrate = 115200)
    print(f'connected to {arduino.name}')
    time.sleep(2)
    arduino.write("h".encode())


while True :
    success , img = cap.read()
    img_copy = img.copy()
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


            #cv2.imshow("test image", img_white)
            prediction , index = classifier.getPrediction(img_white,draw=False)
            print(prediction,index)
            cv2.imshow("Croppedimage" , img_white) # removed in between stage
            cv2.rectangle(img_copy, (x-offset,y-offset) , (x+w+offset,y+h+offset),(255,0,0),2)
            cv2.putText(img_copy , labels[index]+" "+str(round(prediction[index],2)), (x-offset,y-offset),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),2)
            
            if (prediction[index]>0.85):
                if(Test_mode not in [0]):
                    if (labels[index] == "goleft"):
                        arduino.write("l".encode())
                    if (labels[index] == "goright"):
                        arduino.write("r".encode())
            else:
                arduino.write("f".encode())









        except Exception as e:
            print(x,y,h,w)
            print(e)
    else:
        arduino.write("f".encode())
    cv2.imshow("image" , img_copy)

    
    key = cv2.waitKey(1)
    
    if key == ord('e'):
        break
    if key == ord('l'):
        arduino.write("l".encode())
        print("l".encode())
    if key == ord('r'):
        arduino.write("r".encode())
        print("r".encode())

if(Test_mode not in [0]):
    arduino.close()
