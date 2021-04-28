import RPi.GPIO as gpio
import sys, select, termios, tty
import time 

class teleop:
    def __init__(self):
        self.settings = termios.tcgetattr(sys.stdin)
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
        self.pwm1.start(30)
        self.pwm2.start(30)
        msg = """
        Control Your bot!
        ---------------------------
        Moving around:
        q    w    e
        a    s    d

        c : stop the bot
        p : change the duty cycle
        CTRL-C to quit
        """
        print(msg)

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

    def left(self):
        gpio.output(self.pa2,gpio.LOW)
	    time.sleep(0.01)
        gpio.output(self.pb2,gpio.LOW)
	    time.sleep(0.01)
        gpio.output(self.pb1,gpio.LOW)
	    time.sleep(0.01)
        gpio.output(self.pa1,gpio.HIGH)

    def right(self):
        gpio.output(self.pa1,gpio.LOW)
	    time.sleep(0.01)
        gpio.output(self.pb1,gpio.LOW)
	    time.sleep(0.01)
        gpio.output(self.pb2,gpio.LOW)
	    time.sleep(0.01)
        gpio.output(self.pa2,gpio.HIGH)
    
    def hard_left(self):
        gpio.output(self.pb1,gpio.LOW)
	    time.sleep(0.01)
        gpio.output(self.pa2,gpio.LOW)
	    time.sleep(0.01)
        gpio.output(self.pa1,gpio.HIGH)
	    time.sleep(0.01)
        gpio.output(self.pb2,gpio.HIGH)

    def hard_right(self):
        gpio.output(self.pa1,gpio.LOW)
	    time.sleep(0.01)
        gpio.output(self.pb2,gpio.LOW)
	    time.sleep(0.01)
        gpio.output(self.pb1,gpio.HIGH)
	    time.sleep(0.01)
        gpio.output(self.pa2,gpio.HIGH)

    def stop(self):
        gpio.output(self.pa1,gpio.LOW)
        gpio.output(self.pb1,gpio.LOW)
        gpio.output(self.pa2,gpio.LOW)
        gpio.output(self.pb2,gpio.LOW)
           
    def set_pwm(self):
        a=input('Set PWM')
        self.pwm1.ChangeDutyCycle(a)
        self.pwm2.ChangeDutyCycle(a)
        print("duty cycle is changed to: ",a)

    def get_key(self):
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key  
 
    def control(self):
        self.key=self.get_key()
    
        if (self.key=='w'):
            self.forward()

        if (self.key=='s'):
            self.backward()

        if (self.key=='d'):
            self.right()

        if (self.key=='a'):
            self.left()

        if (self.key=='e'):
            self.hard_right()

        if (self.key=='q'):
            self.hard_left()
        
        if (self.key=='c'):
            self.stop()
        
        if (self.key=='p'):
            self.stop()
            self.set_pwm()
            
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
if __name__=='__main__':
    tel=teleop()
    while(True):
        tel.control()
        if (tel.key == '\x03'):
            gpio.cleanup()
            break