import cv2
import numpy as np
import rospy
import time

class colour_detect:     

    def detect(self):
        cap=cv2.VideoCapture(0)
        ret,image=cap.read()
        time.sleep(1)
        cv2.imshow('img',image)
        self.img=image
        self.detected_colour=None  
        cap.release  
        print(ret)       
        if(ret):

            hsv=cv2.cvtColor(self.img,cv2.COLOR_BGR2HSV)
            #definig the range of red color
            red_lower=np.array([136,87,111],np.uint8)
            red_upper=np.array([180,255,255],np.uint8)

            #defining the Range of Blue color
            blue_lower=np.array([99,115,150],np.uint8)
            blue_upper=np.array([110,255,255],np.uint8)
            
            #defining the Range of yellow color
            yellow_lower=np.array([22,60,200],np.uint8)
            yellow_upper=np.array([60,255,255],np.uint8)

            #finding the range of red,blue and yellow color in the image
            red=cv2.inRange(hsv, red_lower, red_upper)
            blue=cv2.inRange(hsv,blue_lower,blue_upper)
            yellow=cv2.inRange(hsv,yellow_lower,yellow_upper)

            kernal=np.ones((5,5),'uint8')

            red=cv2.dilate(red,kernal)
            blue=cv2.dilate(blue,kernal)
            yellow=cv2.dilate(yellow,kernal)

            (_,contours,_)=cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            for _, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if(area>300):
                    detected_colour='R'
                    return (str(detected_colour))

            (_,contours,_)=cv2.findContours(blue,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            for _, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if(area>300):
                    detected_colour='B'
                    return (str(detected_colour))

            (_,contours,_)=cv2.findContours(yellow,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            for _, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if(area>300):
                    detected_colour='Y'
                    return (str(detected_colour))


if __name__=='__main__':
    colour=colour_detect()
    a=colour.detect()
    print(a)