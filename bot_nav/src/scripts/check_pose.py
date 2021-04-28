#! /usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
import tf

class check_pose:
    def pose(self):
        rospy.init_node('check_pose')
        odom_sub = rospy.Subscriber('/odom', Odometry, self.get_pose)
        rospy.spin()

    def get_pose(self,msg):
        self.x=msg.pose.pose.position.x
        self.y=msg.pose.pose.position.y
        quat=msg.pose.pose.pose.orientation
        quat_list=[quat.x,quat.y,quat.z,quat.w]
        (_,_,self.yaw)=tf.transformations.euler_from_quaternion(quat_list)
        return (self.x,self.y,self.yaw)

if __name__=='__main__':
    a=check_pose()
    a.pose()