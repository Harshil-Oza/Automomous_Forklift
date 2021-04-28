import time

class servo_scanner:
    def __init__(self,servo_pin,init_ang,max_ang=180,min_ang=0,n_steps=10,time_min_max=0.5,serial_port="/dev/ttyAMA0"):
        

        self.ang_step= (max_ang-min_ang)/(n_steps-1) # angle each step
        self.min_max_time=time_min_max
        self.servo_speed=(max_ang - min_ang)/(self.min_max_time)
        self.min_pause=self.ang_step/self.servo_speed
        
        self.move_dir=1
        self.init_ang=init_ang
        self.max_ang=max_ang
        self.min_ang=min_ang

    def scan(self,reset=False):
        da=self.min_ang
        init_time=time.time()
        ranges=[]

        while True:
            print(" a="+da)
            ranges.append(da)

            if da==self.max_ang:
                
                break   
            da+=self.ang_step  

        time_increment=(init_time-time.time())/(len(ranges)-1)
        angle_increment=self.ang_step
        time.sleep(self.min_pause)
        return(self.min_ang,self.max_ang,time_increment,angle_increment,ranges)
                
if __name__=="__main__":

    scanner=servo_scanner(12,0)
    time.sleep(1)

    while True:
        print (scanner.scan(reset=True))
