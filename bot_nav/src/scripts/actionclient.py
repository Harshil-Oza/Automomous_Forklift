import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import tf 

class move_base_client:
    def __init__(self):
                # We create some constants with the corresponing vaules from the SimpleGoalState class
        self.PENDING = 0
        self.ACTIVE = 1
        self.PREEMPTED = 2
        self.SUCCEEDED = 3
        self.ABORTED = 4

        action_server_name = '/move_base_client'
        self.client = actionlib.SimpleActionClient(action_server_name, MoveBaseAction)
        # waits until the action server is up and running
        rospy.loginfo('Waiting for action Server ' + action_server_name)
        self.client.wait_for_server()
        rospy.loginfo('Action Server Found...' + action_server_name)
        self.goal=MoveBaseGoal()

    def feedback_cb(self):
        rospy.loginfo("going towards the goal")

    def done_cb(self):
        rospy.loginfo('goal reached')
        rospy.set_param('reached','yes')

    def move_to_goal(self,location):
        self.loc=rospy.get_param(location)
        x=self.loc[0]
        y=self.loc[1]
        ang=self.loc[2]
        self.goal.target_pose.header.frame_id = "map"
        self.goal.target_pose.header.stamp = rospy.Time.now()
        self.goal.target_pose.pose.position.x = x
        self.goal.target_pose.pose.position.y = y
        self.goal.target_pose.pose.orientation=tf.transformations.quaternion_from_euler(0,0,ang)

        self.client.send_goal(self.goal,done_cb=self.done_cb,feedback_cb=self.feedback_cb)

        if(self.client.get_state()==self.PREEMPTED):
            rospy.loginfo('The action has been recieved a cancel request')
        
        if (self.client.get_state()==self.ABORTED):
            rospy.loginfo('The action has been aborted')
        

if __name__=="__main__":
    mb=move_base_client()
    mb.move_to_goal('0R')

        






