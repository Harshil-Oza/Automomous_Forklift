#!/usr/bin/env python
import RPi.GPIO as gpio
import rospy
from std_msgs.msg import Int64

class encoders:
# ------------------------------------------------------------------------------ 
  def __init__(self,r_pin,l_pin,lift_pin):
    rospy.init_node('encoders')
    self.r=rospy.Rate(10)
    self.r_en= r_pin
    self.l_en= l_pin
    self.lift_en=lift_pin

    gpio.setmode(gpio.BOARD)
    gpio.setup(self.r_en,gpio.IN,pull_up_down=gpio.PUD_UP)
    gpio.setup(self.l_en,gpio.IN,pull_up_down=gpio.PUD_UP)
    gpio.setup(self.lift_en,gpio.IN,pull_up_down=gpio.PUD_UP)

    self.r_ticks=0
    self.l_ticks=0
    self.lift_ticks=0

    #initializng publisher
    self.right_enc=rospy.Publisher('rwheel',Int64,queue_size=10)  
    self.left_enc=rospy.Publisher('lwheel',Int64,queue_size=10)
    self.lift_enc=rospy.Publisher('lift_enc',Int64,queue_size=10)
    
#------------------------------------------------------------------------------

  def r_fb(self):
    self.r_ticks+=1

  def l_fb(self):
    self.l_ticks+=1

  def lift_fb(self):
      self.lift_ticks+=1

  def pub_values(self):
    self.right_enc.publish(self.r_ticks)
    self.left_enc.publish(self.l_ticks)
    self.lift_enc.publish(self.lift_ticks)

  def spin(self):
    gpio.add_event_detect(self.r_en, gpio.BOTH, callback=self.r_fb)
    gpio.add_event_detect(self.l_en, gpio.BOTH, callback=self.l_fb)
    gpio.add_event_detect(self.lift_en, gpio.BOTH, callback=self.lift_fb)

    while not rospy.is_shutdown():
      print('r='+self.r_ticks+' l='+self.l_ticks+' lift='+self.lift_ticks)
      en.pub_values()
      self.r.sleep()
    
if __name__ =='__main__':
  en=encoders(36,38,40)
  en.spin()
  
   

