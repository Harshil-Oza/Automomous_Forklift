import RPi.GPIO as gpio
import sys, select, termios, tty
class motor:
    def __init__(self):
        self.settings = termios.tcgetattr(sys.stdin)
        self.en=35
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.en,gpio.OUT)
        self.pwm=gpio.PWM(self.en,100)
        self.pwm.start(100)

    def get_key(self):
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key 

    def spin(self):
        key=self.get_key()
        if key=='p':
            a=input('enter duty cycle')
            self.pwm.ChangeDutyCycle(a)
            
if __name__=="__main__":
   m=motor()
   m.spin() 
