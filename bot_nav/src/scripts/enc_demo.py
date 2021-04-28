import RPi.GPIO as gpio

class encoders:
  def __init__(self,r_pin,l_pin):
    self.r_en= r_pin
    self.l_en= l_pin
    
    self.r_current=0
    self.l_current=0
    
    gpio.setmode(gpio.BOARD)
    gpio.setup(self.r_en,gpio.IN,pull_up_down=gpio.PUD_UP)
    gpio.setup(self.l_en,gpio.IN,pull_up_down=gpio.PUD_UP)
    
    self.r_last_state=gpio.input(self.r_en)
    self.l_last_state=gpio.input(self.l_en)

    self.r_ticks=0
    self.l_ticks=0

  def r_read_en(self):
    self.r_current=gpio.input(self.r_en)
    if ( self.r_current != self.r_last_state ):
        self.r_last_state=self.r_current
        self.r_ticks+=1  
    return self.r_ticks
 
 # def l_read_en(self):
 #   if ( self.l_current=gpio.input(self.l_en) != self.l_last_state ):
 #       self.l_last_state=current_state
 #       l_ticks+=1  
 #   return self.l_ticks

    
if __name__ =='__main__':
   en=encoders(16,18)
   while(True):
     r_en=en.r_read_en()
     #l_en=l_read_en()
     print("Right encoder:",r_en)
     #print("Left encoder:",l_en)
