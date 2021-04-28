from bot_nav.srv import lift_srv
from bot_nav.srv import lift_srvRequest 
from bot_nav.srv import lift_srvResponse
import rospy
import lift_level


def change_level(req):
    lift=lift_level.lift_level(24,26)
    l=lift.update_level(req)
    return(lift_srvResponse(str(req)+str(l)))

def lift_server():
        rospy.init_node('lift_server')
        s= rospy.Service('lift_server', lift_srv, change_level)
        rospy.loginfo("updating level")
        rospy.spin()

if __name__=="__main__":
    lift_server() 