import rospy
import RPi.GPIO as gpio
from math import pi

class distance:
    def __init__(self):
        self.total_ticks_per_revolution=rospy.get_param('total_ticks_per_revolution',45)
        self.wheel_dia=7.8
        self.enc_left=None
        self.enc_right=None
         self.pa1=3                             #pa1= right motor positive
        self.pb1=5			       #pb1= right motor negative
        self.en1=7			       

        self.pa2=11			       #pa2= left motor positive
        self.pb2=13			       #pb2= left motor negative
        self.en2=15

        gpio.setmode(gpio.BOARD)
        gpio.setup(self.pb1,gpio.OUT)
        gpio.setup(self.pa1,gpio.OUT)
        gpio.setup(self.en1,gpio.OUT)
        gpio.setup(self.en2,gpio.OUT)
        gpio.setup(self.pb2,gpio.OUT)
        gpio.setup(self.pa2,gpio.OUT)

        self.pwm1=gpio.PWM(self.en1,40)
        self.pwm2=gpio.PWM(self.en2,40)
        self.pwm1.start(20)
        self.pwm2.start(20)
        
        rospy.Subscriber("lwheel",Int64,self.lwheelcallback)
        rospy.Subscriber("rwheel",Int64,self.rwheelcallback)

    def lwheelcallback(self,msg):
        value=msg.data
        self.left=value

    def rwheelcallback(self,msg):
        value=msg.data
        self.right=value    

     def forward(self):
        gpio.output(self.pb1,gpio.LOW)
	    time.sleep(0.01)
        gpio.output(self.pb2,gpio.LOW)
	    time.sleep(0.01)
        gpio.output(self.pa1,gpio.HIGH)
	    time.sleep(0.01)
        gpio.output(self.pa2,gpio.HIGH)
    
    def backward(self):
        gpio.output(self.pa1,gpio.LOW)
	    time.sleep(0.01)
        gpio.output(self.pa2,gpio.LOw)
    	time.sleep(0.01)
        gpio.output(self.pb1,gpio.HIGH)
	    time.sleep(0.01)
        gpio.output(self.pb2,gpio.HIGH)

    def stop(self):
        gpio.output(self.pa1,gpio.LOW)
        gpio.output(self.pb1,gpio.LOW)
        gpio.output(self.pa2,gpio.LOW)
        gpio.output(self.pb2,gpio.LOW)

    def move(self,distance,dir):                # distance in cm
        self.enc_left=self.right
        self.enc_right=self.left                      
        d=0                             #1 for forward -1 for backward
        #des_ticks=int((distance*self.total_ticks_per_revolution)/pi*self.wheel_dia)
        if (dir==1):
            self.forward()
            while (d<distance):
                d_left= (2*pi*self.wheel_dia*(self.left - self.enc_left))/(self.total_ticks_per_revolution)
                d_right= (2*pi*self.wheel_dia*(self.right - self.enc_right))/(self.total_ticks_per_revolution)
                d=(d_left + d_right)/2
                print(d)
        if (dir==-1):
            self.backward()
            while (d<distance):
                d_left= (2*pi*self.wheel_dia*(self.left - self.enc_left))/(self.total_ticks_per_revolution)
                d_right= (2*pi*self.wheel_dia*(self.right - self.enc_right))/(self.total_ticks_per_revolution)
                d=(d_left + d_right)/2
                print(d)    
        self.stop()

if __name__=="__main__":
    d=distance()
    d.move(20,1)