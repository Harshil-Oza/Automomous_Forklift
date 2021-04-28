import rospy
from location import location
from check_pose import check_pose
from actionclient import move_base_client
from lift_client import lift_client
from distance import distance

class main:
    def __init__(self):
        self.move_base=move_base_client()
        home=rospy.get_param('home')
        self.move_base.move_to_goal(home)
        self.l=location()
        self.dist=distance()
        self.lift=lift_client()
        
    def go_to_loading(self):
        loading=rospy.get_param('loading')
        self.move_base.move_to_goal(loading)

    def go_to_home(self):

        home=rospy.get_param('home')
        self.move_base.move_to_goal(home)

    def main(self):
        self.go_to_loading()
        while(rospy.get_param('reached')=='no'):
            pass
        rospy.set_param('reached','no')
        loc=self.l.locate()
        self.lift.srv_client(0.0)
        self.dist.move(20,1)
        self.lift.srv_client(0.1)
        self.dist.move(20,-1)
        self.move_base.move_to_goal(loc)

        self.lift.srv_client(loc[5])
        self.dist.move(20,1)
        self.lift.srv_client(loc[4])
        self.dist.move(20,-1)
        self.lift.srv_client(0.0)
            
        while(rospy.get_param('reached')=='no'):
            pass
        rospy.set_param('reached','no')
        self.dist.move(20,1)
        self.lift.srv_client(0)
        self.lift.srv_client(loc[3])
        
if __name__=='__main__':
    m=main()
    while(rospy.get_param('load')==True):
        m.main()
    m.go_to_home()