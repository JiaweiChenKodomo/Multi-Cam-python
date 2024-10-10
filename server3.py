'''
Note: This script contacts the server through Port 5000. It is known that
National Instrument's LabView also uses this portal. So tagsrv.exe needs to be
terminated first. This is not a problem on Raspberry Pi.

'''

import socket
import cam_control as cc

# Manually set
# IP address and port of the server controlling the camera.
host = '192.168.2.19'
port = 5000
# If gvfs may hold up the camera.
kill_gvfs = True

########################
# Create a TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)
print("Listening on {}:{}".format(host, port))

def kill_gvfs_process():
    kill_process("gvfs-gphoto2-volume-monitor")
    kill_process("gvfsd-gphoto2")

def kill_process(name):
    # Code learned from https://www.geeksforgeeks.org/kill-a-process-by-name-using-python/
	import os, signal
	# Ask user for the name of process
	try:
		
		# iterating through each instance of the process
		for line in os.popen("ps ax | grep " + name + " | grep -v grep"): 
			fields = line.split()
			
			# extracting Process ID from the output
			pid = fields[0] 
			
			# terminating process 
			os.kill(int(pid), signal.SIGKILL) 
		print("Process Successfully terminated")
		
	except:
		print("Error Encountered while running script")



while True:
    try:
        c, addr = s.accept()
        print("Connection accepted from " + repr(addr))
        instr = c.recv(4096).decode()
        print(repr(addr) + ": " + instr)
        
        if kill_gvfs:
            kill_gvfs_process()
            kill_gvfs = False
        
        if "START" in instr:
            timeStr = cc.focus_start_recording_loud()
            if "ERROR" in timeStr:
                msgStr = timeStr
            else:
                msgStr = "Start recording at " + timeStr
            c.sendall(msgStr.encode())
        elif "TAKE" in instr:
            result = cc.take_one_shot()
            if "ERROR" in result:
                msgStr = result
            else: 
                newFileName = instr[5:]
                timeStr = cc.get_time_tag()
                result = cc.img_rename(newFileName, timeStr[0:19])
                msgStr = result + " shot(s) taken"
                c.sendall(msgStr.encode())
        elif "STOP" in instr:
            newFileName = instr[5:]
            outCode = cc.stop_recording_save_rename(newFileName, timeStr)
            if "ERROR" in outCode:
                msgStr = outCode
            else:
                msgStr = "Stopped and saved"
            c.sendall(msgStr.encode())
        elif "WIPE" in instr:
            result = format_card()
            if result.stderr or "ERROR" in result.stdout:
		        msgStr = result.stderr + result.stdout
            else:
                msgStr = "All data wiped"
                c.sendall(msgStr.encode())
        else:
            msgStr = "Unknown command"
            c.sendall(msgStr.encode())

    except socket.error as e:
        print(f"Socket error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        c.close()

