import numpy as np 
import cv2 as cv
import ASV_Functions as F
import ASV_Parameters as P
import laser2
import maestro 
import time,sys,tty,termios

cap = cv.VideoCapture(0)

cap.set(3,640)
cap.set(4,480)

def webcam():
  while True:
    ret, frame = cap.read()
  
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
  
    lower_color = np.array([190, 50, 50], dtype=np.uint8) #lower color threshold (H,S,V) ~ current values defines blue
    upper_color = np.array([210, 255, 255], dtype=np.uint8) #upper color threshold (H,S,V) ~ current values defines blue

    #Image mask can now be created to get only specified color. Image mask is used to calculate Image moment of object.
    mask = cv.inRange(hsv, lower_color, upper_color)
    moments = cv.moments(mask)

    area = moments['m00']

    #checking area of object before calculating the x and y centroids
    if(area > 100000):
      x = moments['m10'] / area
      y = moments['m01'] / area
    return x, y, area

    # show the output frame
    cv.imshow("Frame", frame)
    key = cv.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
      break

  # do a bit of cleanup
  cv.destroyAllWindows()
  cap.stop()



#ASV movements according to the changes in x and y centroids value

def track(x,y,area):
  x, y, area = webcam()
  distance = laser2.laser_measurement()
  while True:
    if (x > 330):
      print("Turn Right")
      #F.turnRight(0.5)
    elif (x < 310):
      print("Turn Left")
      #F.turnLeft(0.5)
    elif (distance > 100):
      print("Forward")
      #F.Thruster_Values(LDM = 0, Speed_PC=1) #forward
    elif (distance < 100):
      print("Reverse")
      #F.Thruster_Values(LDM = 180, Speed_PC=1) #reverse
  """elif ((310 <= x <= 330) and area < 1500000): #if object too close
    F.Thruster_Values(LDM = 0, Speed_PC=1) #forward
  elif ((310 <= x <= 330) and area > 4000000): #if object too far
    F.Thruster_Values(LDM = 180, Speed_PC=1) #reverse"""