#!/usr/bin/env python
import RPi.GPIO as gpio
import rospy
from std_msgs.msg import Int64

class encoders:
# ------------------------------------------------------------------------------ 
  def __init__(self,r_pin):
    rospy.init_node('encoders')
    self.r=rospy.Rate(10)
    self.r_en= r_pin

    gpio.setmode(gpio.BOARD)
    gpio.setup(self.r_en,gpio.IN,pull_up_down=gpio.PUD_UP)

    self.r_ticks=0
    self.l_ticks=0
    self.lift_ticks=0

    #initializng publisher
    self.right_enc=rospy.Publisher('rwheel',Int64,queue_size=10)  
    
#------------------------------------------------------------------------------

  def r_fb(self):
    self.r_ticks+=1

  def pub_values(self):
    self.right_enc.publish(self.r_ticks)

  def spin(self):
    gpio.add_event_detect(self.r_en, gpio.BOTH, callback=self.r_fb)

    while not rospy.is_shutdown():
      print('r='+self.r_ticks)
      en.pub_values()
      self.r.sleep()
    
if __name__ =='__main__':
  en=encoders(36)
  en.spin()