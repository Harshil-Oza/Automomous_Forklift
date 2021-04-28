from barcode import barcode
import rospy

class location:
    def __init__(self):
        a=barcode()
        self.ID=a.detect_barcode()
        
    def locate(self):
        levels=1
        for i in range(0,levels+1):

            loc=self.colour+'_'+str(i)
            pos=rospy.get_param(loc,default='home')
            if pos[3]=='empty':
                rospy.loginfo('placing in '+loc)
                print('placing in '+loc)
                return (loc)
            if pos[3]=='filled':
                rospy.loginfo(str(loc)+'is occupied')
                print(loc+' is occupied')
            if levels==i:
                rospy.loginfo(self.dict[self.colour] +'color selves are full')
                print(self.dict[self.colour] +' color selves are full')
if __name__=='__main__':
    l=location()
    a=l.locate()
