from barcode import barcode
import rospy
import pandas as pd

class location:
    def locate(self):
        a=barcode()
        ID=a.detect_barcode()
        df=pd.read_csv("database.csv")
        a=df["barcode"]==ID
        pos=df.loc[a,'location'][1]
        return pos
    
if __name__=='__main__':
    l=location()
    a=l.locate()
