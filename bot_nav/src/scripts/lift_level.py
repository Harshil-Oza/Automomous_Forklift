import rospy
import RPi.GPIO as gpio
from std_msgs.msg import Int64

class lift_level:

    def __init__(self,motor_positive,motor_negative):
        self.l_u=motor_positive
        self.l_d=motor_negative
		gpio.setmode(gpio.BOARD)
		gpio.setup(self.lift_en,gpio.IN,pull_up_down=gpio.PUD_DOWN)
		gpio.setup(self.l_u,gpio.OUT)
		gpio.setup(self.l_d,gpio.OUT)
		gpio.output(self.l_u,gpio.HIGH)
		gpio.output(self.l_d,gpio.HIGH)
		self.lift_ticks=0
        self.levels={0.0:0, 0.1:251, 1.0:4000, 1.1:4040}  
        rospy.set_param('lift_level',0.0)
        rospy.Subscriber("lift_enc",Int64, self.lift_callback)

    def up(self):
        gpio.output(self.motor_positive,gpio.HIGH)
        gpio.output(self.motor_negative,gpio.LOW)

    def down(self):
        gpio.output(self.motor_positive,gpio.LOW)
        gpio.output(self.motor_negative,gpio.HIGH)

    def stop(self):
        gpio.output(self.motor_positive,gpio.LOW)
        gpio.output(self.motor_negative,gpio.LOW)

    def lift_callback(self,msg):
        value=msg.data
        self.lift_ticks=value
    
    def update_level(self, des_level):
        current_level=rospy.get_param('lift_level')      #values in the parameter server
        init_ticks=self.lift_ticks

        if (current_level!=des_level):                       
            if(float(des_level)>float(current_level)):          #to decide whether to go up or down
                level_ticks=abs(self.levels[des_level] - self.levels[current_level])

                while( (self.lift_ticks-init_ticks) != level_ticks ):
                    self.up()
                self.stop()
                rospy.set_param('lift_level',des_level)
                return ('reached')

            elif (float(des_level)<float(current_level)):
                level_ticks=abs(self.levels[des_level] - self.levels[current_level])

                while( (self.lift_ticks-init_ticks) != level_ticks ):
                    self.down()
                self.stop()
                rospy.set_param('lift_level',des_level)      #update level
                return('reached')

        else:
            print("already on the same level")

if __name__=='__main__': 
    lift=lift_level(33,35)
	a=input("des_level:")
	lift.update_level(a)

        

        