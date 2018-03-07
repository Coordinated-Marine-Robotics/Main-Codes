import ASV_Functions as F
import ASV_Parameters as P
import numpy as np
import imu
import laser2
import maestro 
import time

get_Camera_Distance = F.get_Camera_Distance()

max_value = 2500*4 #maximum speed desired for clockwise rotation
min_value = 500*4  #minimum speed desired for anti-clockwise rotation

servo = maestro.Controller()
servo.setRange(0, min_value, max_value)
servo.setRange(1, min_value, max_value)
servo.setRange(2, min_value, max_value)
#Initializing motor
servo.setTarget(0,6000)
servo.setTarget(1,6000)
servo.setTarget(2,6000)
time.sleep(1)

def start():
	
	while("detection" == True):		#need to add when object is detected
		if camera_centre != object_centre: #need to include frame centre from foam.py
			while(object_centre < camera_centre):
				turnLeft(0.5)
			else:
				turnRight(0.5)

		#Keep a constant distance between target object
		while(get_Camera_Distance == True):
			if distance > 100:
				F.Thruster_Values(LDM = 0, Speed_PC=1) # move forwards
			else:
				F.Thruster_Values(LDM = 180, Speed_PC=1) # move backwards
		while(get_Camera_Distance == False):
			F.turnRight(1)




def stop(): #This will stop every action your Pi is performing for ESC ofcourse.
    servo.setTarget(0,6000)
    servo.setTarget(1,6000)
    servo.setTarget(2,6000)
    servo.close()
    print("Okay")


#Starting the program
inp = input()
if inp == "start":
    start()
elif inp == "stop":
    stop()
else :
    print ("Error. Restart from beginning.")