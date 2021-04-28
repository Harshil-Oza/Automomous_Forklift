import time
import servo_pi
import tf_mini
import math

class servo_scanner:
    def __init__(self,servo_pin=13,init_ang=0,max_ang=180,min_ang=0,n_steps=10,time_min_max=0.5,serial_port="/dev/ttyS0"):
        self.ser=servo_pi.servo(servo_pin,init_ang)
        self.laser=tf_mini.TfMini(serial_port)

        self.ang_step= (max_ang-min_ang)/(n_steps-1) # angle each step
        self.min_max_time=time_min_max
        self.servo_speed=(max_ang - min_ang)/(self.min_max_time)
        self.min_pause=self.ang_step/self.servo_speed
        
        self.move_dir=1
        self.init_ang=init_ang
        self.max_ang=max_ang
        self.min_ang=min_ang
        self.n_steps=n_steps

       
    def read_laser(self):
        return(self.laser.get_data())
    
    def reset_servo(self):
        self.ser.reset()
        self.move_dir=1
        time.sleep(0.2)

    def scan(self,scale_factor=0.01 ,reset=False):
        if reset: self.reset_servo()
        da=self.min_ang
        init_time=time.time()
        ranges=[]

        for _ in range(self.n_steps):
            dist=self.read_laser()
            #print("d=%f a=%f"%(dist,da))
            ranges.append(dist)

            self.ser.update(da)
            time.sleep(self.min_pause)
            if da==self.max_ang:
                break 
            da+=self.ang_step  

        time_increment=(time.time()-init_time)/(len(ranges)-1)
        angle_increment=self.ang_step
        self.reset_servo()
        
        return(self.min_ang,self.max_ang,time_increment,angle_increment,ranges)
if __name__=="__main__":

    scanner=servo_scanner()
    scanner.reset_servo()
    time.sleep(1)

    while True:
        print (scanner.scan(reset=True))
