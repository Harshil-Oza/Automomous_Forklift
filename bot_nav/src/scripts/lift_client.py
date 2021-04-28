from bot_nav.srv import lift_srv
from bot_nav.srv import lift_srvRequest 
from bot_nav.srv import lift_srvResponse
import rospy

class lift_client:
    def srv_client(self,level):
        rospy.wait_for_service('lift_server')
        try:
            lift_service=rospy.ServiceProxy('lift_service',lift_srv)
            res=lift_service(level)
            return (res.result)
        except rospy.ServiceException as e:
            print("Service call failed",e)

if __name__=='__main__':
    l=lift_client()
    l.srv_client(1) 