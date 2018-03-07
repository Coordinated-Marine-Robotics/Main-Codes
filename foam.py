# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 13:12:18 2018

@author: Syafiqah
"""

import numpy as np
import cv2 as cv
#import argparse

def nothing(x):
    pass
cv.namedWindow('colour range', cv.WINDOW_NORMAL)
#blue: h [60-120] s[40 203], v[26 217]
h,s,v = 100,100,100
cv.createTrackbar('h', 'colour range',85,179,nothing)
cv.createTrackbar('s', 'colour range',70,255,nothing)
cv.createTrackbar('v', 'colour range',100,255,nothing)
cv.createTrackbar('hu', 'colour range',120,190,nothing)
cv.createTrackbar('su', 'colour range',203,255,nothing)
cv.createTrackbar('vu', 'colour range',255,255,nothing)
#red = np.uint8([[[0,0,255 ]]])
#hsv_red = cv2.cvtColor(red,cv2.COLOR_BGR2HSV)
#print (hsv_red) = [[[  0 255 255]]] ,183

vid = cv.VideoCapture(1)

while(True):
	ret, frame = vid.read()
	median = cv.medianBlur(frame,9)
	gray = cv.GaussianBlur(frame, (11,11),0)
	hsvt = cv.cvtColor(gray,cv.COLOR_BGR2HSV)
	hsvt2 = cv.cvtColor(median,cv.COLOR_BGR2HSV)
	
	h = cv.getTrackbarPos('h','colour range')
	s = cv.getTrackbarPos('s','colour range')
	v = cv.getTrackbarPos('v','colour range')
	hu = cv.getTrackbarPos('hu','colour range')
	su = cv.getTrackbarPos('su','colour range')
	vu = cv.getTrackbarPos('vu','colour range')
	lower_obj = np.array([h,s,v])
	upper_obj = np.array([hu,su,vu])
	
	mask = cv.inRange(hsvt, lower_obj, upper_obj)
	mask = cv.erode(mask, None, iterations=2)
	mask = cv.dilate(mask, None, iterations=2)
	
	mask2 = cv.inRange(hsvt2, lower_obj, upper_obj)
	mask2 = cv.erode(mask2, None, iterations=2)
	mask2 = cv.dilate(mask2, None, iterations=2)

	cnts = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	if len(cnts)>0:
		c = max(cnts, key=cv.contourArea)
		((x, y), radius) = cv.minEnclosingCircle(c)
		M = cv.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		if radius > 10:
			cv.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
			cv.circle(frame, center, 5, (0, 0, 255), -1)
	(minVal2, maxVal2, minLoc2, maxLoc2) = cv.minMaxLoc(mask)
	res = cv.bitwise_and(frame,frame, mask= mask)
	res2 = cv.bitwise_and(frame,frame, mask= mask2)
	(minVal, maxVal, minLoc, maxLoc) = cv.minMaxLoc(mask2)
	#cv.circle(frame, maxLoc2, 10, (255,0,0), 2)
	#cv.circle(frame, maxLoc, 10, (255,255,0), 2)
	cv.imshow("ori", frame)
	#cv.imshow('median', median)
	cv.imshow('resmed', res2)
	#cv.imshow("gray", gray)
	cv.imshow("res", res)
	#print ("h = %s, s=%s, v=%s" %h %s %v)
	if cv.waitKey(20) == 27: # 27 is ESC key
		break

vid.release()
cv.destroyAllWindows()
