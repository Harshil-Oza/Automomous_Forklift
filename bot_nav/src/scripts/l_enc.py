#!/usr/bin/env python
import RPi.GPIO as gpio
import rospy
from std_msgs.msg import Int64

class encoders:
# ------------------------------------------------------------------------------ 
  def __init__(self,l_pin):
    rospy.init_node('encoders')
    self.r=rospy.Rate(10)
    self.l_en= l_pin

    gpio.setmode(gpio.BOARD)
    gpio.setup(self.l_en,gpio.IN,pull_up_down=gpio.PUD_UP)

    self.l_ticks=0
    #initializng publisher 
    self.left_enc=rospy.Publisher('lwheel',Int64,queue_size=10)
   
#------------------------------------------------------------------------------

  def l_fb(self):
    self.l_ticks+=1

  def pub_values(self):
    self.left_enc.publish(self.l_ticks)

  def spin(self):
    gpio.add_event_detect(self.l_en, gpio.BOTH, callback=self.l_fb)

    while not rospy.is_shutdown():
      print('r='+self.l_ticks)
      en.pub_values()
      self.r.sleep()
    
if __name__ =='__main__':
  en=encoders(38)
  en.spin()