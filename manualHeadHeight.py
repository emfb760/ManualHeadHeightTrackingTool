#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import sys
import os
from guiWindow import *
import datetime

CAP_PROP_POS_MSEC = 0

fileName = ""
camera = ""
startFrame = 0
endFrame = 99999

headLocList = []
currTime = -1

log = ""

def printAndLog(str):
	global log
	log = log + "\n" + str
	print str
	sys.stdout.flush()
	
def printHeadLocList():    
	f = open(fileName+"_manualHeadHeight.csv", 'w')
	f.write("time(ms),height\n")
	for headLoc in headLocList:
		f.write(str(headLoc[0]) + "," + str(headLoc[1]) + "\n")
	
	f.close()
	
	f = open(fileName+"_manualHeadHeight.log", 'w')
	f.write("Session completed at ")
	f.write(datetime.datetime.now().strftime("%I:%M:%S %p on %b %d, %Y"))
	f.write("\n\n")
	f.write(log)
	f.close()

	
def end_program():	
	printAndLog("End of video reached.")
	printAndLog("Results saved to %s_manualHeadHeight.csv"%(fileName))
	printAndLog("Logfile saved to %s_manualHeadHeight.log"%(fileName))
	printHeadLocList()
	sys.exit(0)
	
#What is executed when the 'No Actor' button is pressed
def executeNoActor(N):
	global headLocList
	global currTime
	
	numFrames = 0
		
	#Make sure that the value for N is an integer
	try:
		numFrames = int(N)
	except ValueError:
		printAndLog("Please type in an integer for N")
		sys.stdout.flush()
		return
	
	#Make sure that the value for N is greater than 0
	if numFrames <= 0:
		printAndLog("Please type in an integer greater than 0 for N")
		return
	
	for i in range(numFrames):
		headLocList.append((currTime,-1))
		
		f, img = camera.read()
		f, img = camera.read()
		currTime = camera.get(CAP_PROP_POS_MSEC)
		
		if not f:
			printAndLog("No Actor option applied to %d frame(s)."%(i+1))
			end_program()
		
	printAndLog("No Actor option applied to %d frame(s)."%(numFrames))
	
	cv2.imshow("video", img)
	

#What is executed when the 'Set Height' button is pressed
def executeSetHeight(N):
	global headLocList
	global currTime
		
	idx = -1
	for b in pose_buttons:
		if b.selected == True:
			idx = b.id
			break
			
	#Extra check to make sure the user has one of the poses selected
	if idx == -1:
		printAndLog("Please select the closest position to which the actor is posed in this frame. If the actor is not on scene, click the 'No Actor' button")
	else:
		numFrames = 0
		
		#Make sure that the value for N is an integer
		try:
			numFrames = int(N)
		except ValueError:
			printAndLog("Please type in an integer for N")
			return
		
		#Make sure that the value for N is greater than 0
		if numFrames <= 0:
			printAndLog("Please type in an integer greater than 0 for N")
			return
	
	
		for i in range(numFrames):
			headLocList.append((currTime,height[idx]))
		
			f, img = camera.read()
			f, img = camera.read()
			currTime = camera.get(CAP_PROP_POS_MSEC)
	
			if not f:
				printAndLog("Height recorded for %d frame(s)."%(i+1))
				end_program()
		
		printAndLog("Height recorded for %d frame(s)."%(numFrames))
		
		cv2.imshow("video", img)


def main():
	global fileName
	global camera
	global currTime
	
	if len(sys.argv) != 2:
		for file in os.listdir("."):
			if file.endswith(".wmv"):
				fileName = file
				break
		if fileName == "":
			printAndLog("Video file not found")
			val = raw_input("Press any key to exit...")
			sys.exit(0)
	else:
		fileName = sys.argv[1]
	
	camera = cv2.VideoCapture(fileName)
	f, img = camera.read()
	f, img = camera.read()
	currTime = camera.get(CAP_PROP_POS_MSEC)
		
	if not f:
		end_program()
			
	cv2.imshow("video", img)
	
	
	app = QtGui.QApplication(sys.argv)
	
	wndw = Wndw(printHeadLocList,executeNoActor,executeSetHeight)
	
	sys.exit(app.exec_())
	
if __name__ == "__main__":
	main()