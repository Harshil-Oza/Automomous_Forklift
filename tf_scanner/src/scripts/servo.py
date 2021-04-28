import RPi.GPIO as gpio  

class servo:    
    def __init__(self,pin,start_angle):
        self.s_dc=1./20. *(start_angle)+1
        gpio.setmode(gpio.BOARD)
        self.pin_no=pin
        gpio.setup(self.pin_no,gpio.OUT)
        self.pwm=gpio.PWM(self.pin_no , 50)
        self.pwm.start(self.s_dc)

    def reset(self):
        self.pwm.ChangeDutyCycle(self.s_dc)

    def update(self,d_ang):
        self.dc=1./20. *(d_ang)+1
        self.pwm.ChangeDutyCycle(self.dc)

    def cleanup(self):
        self.pwm.stop()
        gpio.cleanup()
    
  
if __name__ == '__main__':
      ser=servo(13,0)
      for i in range(5):
          d_pos=input("enter")
          ser.update(d_pos)
      gpio.cleanup()
