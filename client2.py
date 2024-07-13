'''
Note: This script contacts the server through Port 5000. It is known that
National Instrument's LabView also uses this portal. So tagsrv.exe needs to be
terminated first. This is not a problem on Raspberry Pi.

This version has more than one sensor.
'''

import socket
import time

port = 5000
serverIPLst = ['192.168.2.19','192.168.2.20','192.168.2.21']
camNameLST = ['Cam1','Cam2','Cam3']

def decode_config_message(msg_bit):
    """Decode and remove all non-ASCII char's."""
    return ''.join([x for x in msg_bit.decode() if ord(x) < 127 and ord(x) > 31])

def reconnect(ServerIp, PORT):
    """Reconnect"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
    server_address = (ServerIp, PORT)
    server_socket.connect(server_address)
    return server_socket

def send_data(server_socket, data_str):
    server_socket.sendall(data_str.encode())

def receive_data(server_socket):
    flag = False
    start_time = time.time()
    while True:
        try:
            receive_data = server_socket.recv(4096)
            print(receive_data)
            real_data = decode_config_message(receive_data)
            print(f'The message is {real_data}')
            if len(real_data) > 0:
                flag = True
                break
        except socket.error as e:
            print(f"Socket error: {e}")
            break

        now_time = time.time()
        if now_time - start_time > 1:
            break
    return flag

while True:
    instr = input("Type 'START' to start all recordings. 'STOP saveFileName' to stop and save file to the saveFileName. 'TAKE saveFileName' to take one shot and save file. CANCEL to terminate program. \n")
    if "START" in instr or "STOP" in instr or "TAKE" in instr:
        for serverIP, camName in zip(serverIPLst, camNameLST):
            try:
                server_socket = reconnect(serverIP, port)
                instr2 = instr + "_" + camName
                send_data(server_socket, instr2)
                if receive_data(server_socket):
                    print("Successful communication!")
                server_socket.close()
            except socket.error as e:
                print(f"Error connecting to {serverIP}:{port} - {e}")
    elif "CANCEL" in instr:
        break



