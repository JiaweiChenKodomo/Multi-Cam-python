'''
Note: This library wraps the code to control the Canon camera via Canon EDSDK.
'''

import os
import subprocess as sp
import datetime

def format_card(cardSlot = "1", camNo = "1"):
	result = sp.run(["./MultiCamCui", camNo, "31", cardSlot], capture_output = True, text = True)
	return result

def download_all(camNo = "1"):
	result = sp.run(["./MultiCamCui", camNo, "30"], capture_output = True, text = True)
	return result

def start_recording(camNo = "1"):
	result = sp.run(["./MultiCamCui", camNo, "40"], capture_output = True, text = True)
	return result

def take_one_shot(camNo = "1"):
	result = refocus(camNo)
	if result.stderr or "ERROR" in result.stdout:
		return "ERROR with refocusing" + result.stderr + result.stdout
	result = sp.run(["./MultiCamCui", camNo, "20"], capture_output = True, text = True)
	return result

def stop_recording(camNo = "1"):
	result = sp.run(["./MultiCamCui", camNo, "41"], capture_output = True, text = True)
	return result

def refocus(camNo = "1"):
	result = sp.run(["./MultiCamCui", camNo, "4"], capture_output = True, text = True)
	return result

def format_start_recording(cardSlot = "1", camNo = "1"):
	print("Not good logic. Will be removed later.")
	format_card(cardSlot, camNo)
	refocus(camNo)
	timeStr = get_time_tag()
	start_recording(camNo)
	return timeStr

def focus_start_recording_loud(camNo = "1"):
	result = refocus(camNo)
	if result.stderr or "ERROR" in result.stdout:
		return "CC_ERROR with refocusing" + result.stderr + result.stdout
	result = start_recording(camNo)
	if result.stderr or "ERROR" in result.stdout:
		return "ERROR with starting recording" + result.stderr + result.stdout
	timeStr = get_time_tag()
	return timeStr

def stop_recording_save_rename(newFileName, stTimeStr, cardSlot = "1", camNo = "1"):
	result = stop_recording(camNo)
	if result.stderr or "ERROR" in result.stdout:
		return "ERROR with stopping recording" + result.stderr + result.stdout
	return save_rename(newFileName, stTimeStr, cardSlot, camNo)

def save_rename(newFileName, stTimeStr, cardSlot = "1", camNo = "1"):
	result = download_all(camNo)
	if result.stderr or "ERROR" in result.stdout:
		return "ERROR with downloading recording" + result.stderr + result.stdout
	pathName = "./cam"+camNo+"/card"+cardSlot+"/"
	newDir = stTimeStr[0:19]
	file_count = 0
	for fileName in os.listdir(pathName):
		if "MVI" in fileName or "IMG" in fileName or "jpg" in fileName or "MOV" in fileName: 
			renameName = newFileName+"_"+fileName
			os.renames(os.path.join(pathName, fileName), os.path.join(pathName, newDir, renameName))
			file_count += 1
	return str(file_count)

def img_rename(newFileName, stTimeStr, cardSlot = "1", camNo = "1"):
	pathName = "./cam"+camNo
	newDir = stTimeStr[0:19]
	file_count = 0
	for fileName in os.listdir(pathName):
		if "IMG" in fileName or "jpg" in fileName: 
			renameName = newFileName+"_"+fileName
			os.renames(os.path.join(pathName, fileName), os.path.join(pathName, newDir, renameName))
			file_count += 1
	return str(file_count)

def get_time_tag():
	timenow = datetime.datetime.now()
	filename = str(timenow)
	filename = filename.replace(' ','_')
	filename = filename.replace(':','-')
	return filename
