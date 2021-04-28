import RPi.GPIO as gpio
import sys, select, termios, tty

class teleop:
    def __init__(self):
        self.settings = termios.tcgetattr(sys.stdin)
        self.motor1_positive=3
        self.motor1_negative=5
        self.motor1_pwm=7

        self.motor2_positive=11
        self.motor2_negative=13
        self.motor2_pwm=15

        gpio.setmode(gpio.BOARD)
        gpio.setup(self.motor1_negative,gpio.OUT)
        gpio.setup(self.motor1_positive,gpio.OUT)
        gpio.setup(self.motor1_pwm,gpio.OUT)
        gpio.setup(self.motor2_pwm,gpio.OUT)
        gpio.setup(self.motor2_negative,gpio.OUT)
        gpio.setup(self.motor2_positive,gpio.OUT)

        self.pwm1=gpio.PWM(self.motor1_pwm,100)
        self.pwm2=gpio.PWM(self.motor2_pwm,100)
        self.pwm1.start(0)
        self.pwm2.start(0)
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
        gpio.output(self.motor1_positive,gpio.HIGH)
        gpio.output(self.motor1_negative,gpio.LOW)
        gpio.output(self.motor2_positive,gpio.HIGH)
        gpio.output(self.motor2_negative,gpio.LOW)
    
    def backward(self):
        gpio.output(self.motor1_positive,gpio.LOW)
        gpio.output(self.motor1_negative,gpio.HIGH)
        gpio.output(self.motor2_positive,gpio.LOW)
        gpio.output(self.motor2_negative,gpio.HIGH)

    def left(self):
        gpio.output(self.motor1_positive,gpio.HIGH)
        gpio.output(self.motor1_negative,gpio.LOW)
        gpio.output(self.motor2_positive,gpio.LOW)
        gpio.output(self.motor2_negative,gpio.LOW)

    def right(self):
        gpio.output(self.motor1_positive,gpio.LOW)
        gpio.output(self.motor1_negative,gpio.LOW)
        gpio.output(self.motor2_positive,gpio.HIGH)
        gpio.output(self.motor2_negative,gpio.LOW)
    
    def hard_left(self):
        gpio.output(self.motor1_positive,gpio.HIGH)
        gpio.output(self.motor1_negative,gpio.LOW)
        gpio.output(self.motor2_positive,gpio.LOW)
        gpio.output(self.motor2_negative,gpio.HIGH)

    def hard_right(self):
        gpio.output(self.motor1_positive,gpio.LOW)
        gpio.output(self.motor1_negative,gpio.HIGH)
        gpio.output(self.motor2_positive,gpio.HIGH)
        gpio.output(self.motor2_negative,gpio.LOW)

    def stop(self):
        gpio.output(self.motor1_positive,gpio.LOW)
        gpio.output(self.motor1_negative,gpio.LOW)
        gpio.output(self.motor2_positive,gpio.LOW)
        gpio.output(self.motor2_negative,gpio.LOW)
           
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