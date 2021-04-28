# -*- coding: utf-8 -*-
import imutils
from pyzbar import pyzbar
import argparse
import datetime 
import time 
import cv2
import csv
import urllib
import numpy as np

class barcode:
	def __init__(self):
		self.url="http://192.168.43.87:8080/shot.jpg"

	def detect_barcode(self):
			imgPath=urllib.urlopen(self.url)
			imgNp=np.array(bytearray(imgPath.read()),dtype=np.uint8)
			img=cv2.imdecode(imgNp,-1)
			frame=imutils.resize(img,width=400)
			barcodes=pyzbar.decode(frame)
			print(barcodes)	
			for barcode in barcodes:
				barcodedata=barcode.data.decode("utf-8")
				#print(barcodedata)
				time.sleep(2)
			return barcodedata
if __name__=='__main__':
    l=barcode()
    a=l.detect_barcode()
