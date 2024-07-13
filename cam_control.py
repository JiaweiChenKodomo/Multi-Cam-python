'''
Note: This library wraps the code to control the Canon camera via Canon EDSDK.
'''

import os
import subprocess as sp
import datetime

def format_card(cardSlot = "1", camNo = "1"):
	sp.run(["./MultiCamCui", camNo, "31", cardSlot])

def download_all(camNo = "1"):
	sp.run(["./MultiCamCui", camNo, "30"])

def start_recording(camNo = "1"):
	sp.run(["./MultiCamCui", camNo, "40"])

def take_one_shot(camNo = "1"):
	refocus(camNo)
	sp.run(["./MultiCamCui", camNo, "20"])

def stop_recording(camNo = "1"):
	sp.run(["./MultiCamCui", camNo, "41"])

def refocus(camNo = "1"):
	sp.run(["./MultiCamCui", camNo, "4"])

def format_start_recording(cardSlot = "1", camNo = "1"):
	format_card(cardSlot, camNo)
	refocus(camNo)
	timeStr = get_time_tag()
	start_recording(camNo)
	return timeStr

def stop_recording_save_rename(newFileName, stTimeStr, cardSlot = "1", camNo = "1"):
	stop_recording(camNo)
	#edTimeStr = get_time_tag()
	return save_rename(newFileName, stTimeStr, cardSlot, camNo)

def save_rename(newFileName, stTimeStr, cardSlot = "1", camNo = "1"):
	#stop_recording(camNo)
	#edTimeStr = get_time_tag()
	download_all(camNo)
	pathName = "./cam"+camNo+"/card"+cardSlot+"/"
	newDir = stTimeStr[0:19]
	for fileName in os.listdir(pathName):
		if "MVI" in fileName or "IMG" in fileName or "jpg" in fileName or "MOV" in fileName: 
			renameName = newFileName+"_"+fileName
			os.renames(os.path.join(pathName, fileName), os.path.join(pathName, newDir, renameName))
	return 0

def img_rename(newFileName, stTimeStr, cardSlot = "1", camNo = "1"):
	pathName = "./cam"+camNo
	newDir = stTimeStr[0:19]
	for fileName in os.listdir(pathName):
		if "IMG" in fileName or "jpg" in fileName: 
			renameName = newFileName+"_"+fileName
			os.renames(os.path.join(pathName, fileName), os.path.join(pathName, newDir, renameName))
	return 0

def get_time_tag():
	timenow = datetime.datetime.now()
	filename = str(timenow)
	filename = filename.replace(' ','_')
	filename = filename.replace(':','-')
	return filename
