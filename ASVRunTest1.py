import ASV_Functions as F
import ASV_Parameters as P
import numpy as np
import imu
import laser2
import maestro 
import time,sys,tty,termios
import foam

#get_Camera_Distance = F.get_Camera_Distance()

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

print("start, controls or stop")

"""def start():
	foam.webcam()
	while(foam.detection == True):		#need to add when object is detected
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
			F.turnRight(1)"""


def getch():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd,termios.TCSADRAIN,old_settings)
	return ch


def controls():
	while True:
		char = getch()
		if(char=="w"):
			F.Thruster_Values(LDM = 0, Speed_PC=1) #forward
		elif(char=="s"):
			F.Thruster_Values(LDM = 180, Speed_PC=1) #backward
		elif(char=="d"):
			F.Thruster_Values(LDM = 90, Speed_PC=1) #move right
		elif(char=="a"):
			F.Thruster_Values(LDM = -90, Speed_PC=1) #move left
		elif(char=="e"):
			F.turnRight(1)
		elif(char=="q"):
			F.turnLeft(1)
		elif(char=="h"):
			stop()
			break


def control_speed(): 
    print ("I'm Starting the motor, I hope its calibrated and armed.")
    time.sleep(1)
    speed1 = 1500*4    # change your speed if you want to.... it should be between 700 - 2000
    speed2 = 1500*4
    speed3 = 1500*4
    print ("Controls - a to decrease speed & d to increase speed OR q to decrease a lot of speed & e to increase a lot of speed")
    while True:
        servo.setTarget(0,speed1)
		servo.setTarget(1,speed2)
		servo.setTarget(2,speed3)
        inp = input()
        
        if inp == "a":
            speed1 -= 10    # decrementing the speed like hell
            print ("speed = %d" % speed1)
        elif inp == "q":    
            speed1 += 10    # incrementing the speed like hell
            print ("speed = %d" % speed1)
        elif inp == "w":
            speed2 += 10     # incrementing the speed 
            print ("speed = %d" % speed2)
        elif inp == "s":
            speed2 -= 10     # decrementing the speed
            print ("speed = %d" % speed2)
        elif inp == "e":
            speed3 += 10     # incrementing the speed 
            print ("speed = %d" % speed3)
        elif inp == "d":
            speed3 -= 10     # decrementing the speed
            print ("speed = %d" % speed3)
        elif inp == "stop":
            stop()          #going for the stop function
            break
        elif inp == "manual":
            manual_drive()
            break
        elif inp == "arm":
            arm()
            break	
        else:
            print ("WHAT DID I SAID!! Press a,q,d or e")


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
elif inp == "controls":
	controls()
elif inp == "speed":
	control_speed()
elif inp == "stop":
    stop()
else :
    print ("Error. Restart from beginning.")