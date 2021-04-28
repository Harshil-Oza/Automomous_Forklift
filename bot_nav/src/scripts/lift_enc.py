#!/usr/bin/env python
from imutils.video import VideoStream
import RPi.GPIO as gpio
import rospy
from std_msgs.msg import Int64

class encoders:
# ------------------------------------------------------------------------------ 
  def __init__(self,lift_pin):
    rospy.init_node('encoders')
    self.r=rospy.Rate(10)
    self.lift_en=lift_pin

    gpio.setmode(gpio.BOARD)
    gpio.setup(self.lift_en,gpio.IN,pull_up_down=gpio.PUD_UP)

    self.lift_ticks=0

    #initializng publisher
    self.lift_enc=rospy.Publisher('lift_enc',Int64,queue_size=10)
    
#------------------------------------------------------------------------------

  def lift_fb(self):
      self.lift_ticks+=1

  def pub_values(self):
    self.lift_enc.publish(self.lift_ticks)

  def spin(self):
    gpio.add_event_detect(self.lift_en, gpio.BOTH, callback=self.lift_fb)

    while not rospy.is_shutdown():
      print('lift='+self.lift_ticks)
      en.pub_values()
      self.r.sleep()
    
if __name__ =='__main__':
  en=encoders(40)
  en.spin()