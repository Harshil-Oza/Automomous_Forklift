#!/usr/bin/env python
import encoders
from math import sin
from math import pi 
from math import cos
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from std_msgs.msg import Int64
from tf.broadcaster import TransformBroadcaster

class odo_diff:
#------------------------------------------------------------------------    
    def __init__(self):
        rospy.init_node('odo_diff')
        rospy.loginfo(rospy.get_name())
        #paraneter for the parameter server
        self.rate=rospy.get_param('~rate',10.0)
        #self.ticks_meter=rospy.get_param('ticks_meter',)
        self.total_ticks_per_revolution=rospy.get_param('total_ticks_per_revolution',45)
        self.wheel_dia=rospy.get_param('wheel_dia',0.078)
        self.base_width=rospy.get_param('base_width',0.385)

        self.base_frame_id='chassis'
        self.odom_frame_id='odom'

        self.left=0
        self.right=0
        self.enc_left=None
        self.enc_right=None
        self.prev_left=0
        self.prev_right=0
        self.x=0
        self.y=0
        self.th=0
        self.l_vel=0
        self.a_vel=0
        self.current_time=rospy.Time.now()
        self.last_time=rospy.Time.now()


        #Publishers and Subcribers
        rospy.Subscriber("lwheel",Int64,self.lwheelcallback)
        rospy.Subscriber("rwheel",Int64,self.rwheelcallback)

        self.odompub=rospy.Publisher('odom',Odometry,queue_size=10)
        self.odombroadcaster=TransformBroadcaster()
#------------------------------------------------------------------------

    def lwheelcallback(self,msg):
        value=msg.data
        self.left=value
#------------------------------------------------------------------------

    def rwheelcallback(self,msg):
        value=msg.data
        self.right=value    
#------------------------------------------------------------------------

    def spin(self):
        r=rospy.Rate(self.rate)
        while not rospy.is_shutdown():
            self.update()
            r.spin()
#-------------------------------------------------------------------------

    def update(selfs):
        now=rospy.Time.now()
        t_elapsed=(now - self.last_time).to_sec()
        self.last_time=now

        #calculating odometry 
        if self.enc_left==None:
            d_left=0
            d_right=0

        else:
            d_left= (2*pi*self.wheel_dia*(self.left - self.enc_left))/(self.total_ticks_per_revolution)
            d_right= (2*pi*self.wheel_dia*(self.right - self.enc_right))/(self.total_ticks_per_revolution)

        self.enc_left=self.left
        self.enc_right=self.right

        #Avg of the distance traveled by both the wheels
        d=(d_left + d_right)/2

        #calculating theta (valid for small angles)
        delta_th=(self.d_right - self.d_left)/self.base_width

        #calculating velocites
        self.l_vel=d/t_elapsed
        self.a_vel=th/t_elapsed
        
        if(d!=0):
            delta_x=cos(delta_th)*d
            delta_y=-sin(delta_th)*d

            self.x = self.x + ( cos( self.th ) * delta_x - sin( self.th ) * delta_y )
            self.y = self.y + ( sin( self.th ) * delta_x + cos( self.th ) * delta_y )
        
        if (th!=0):
            self.th=self.th + delta_th

        #converting euler to quaternion
        odom_quat=tf.transformations.quaternion_from_euler(0,0,self.th)

        #publishing odometry
        self.odombroadcaster.sendTransform((self.x,self.y,0),odom_quat,rospy.Time.now(),self.base_frame_id,self.odom_frame_id)

        odom=Odometry()
        odom.header.stamp=now
        odom.header.frame_id=self.odom_frame_id
        odom.child_frame_id=self.child_frame_id
        odom.pose.pose.position.x=self.x
        odom.pose.pose.position.y=self.y
        odom.pose.pose.position.z=0
        odom.pose.pose.orientation=odom_quat    
        odom.twist.twist.linear.x=self.l_vel
        odom.twist.twist.linear.y=0
        odom.twist.twist.linear.x=self.a_vel

        self.odomPub.publish(odom)
#---------------------------------------------------------------------------------------------

if __name__=='__main__':
    odo_diff=odo_diff()
    odo_diff.spin()