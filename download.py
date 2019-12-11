'''
This script uses some pretty abstract ideas to get the book. I understand it might not be the best way, but I had trouble finding other ways.
you may need to go through and fix some integers where pyautogui is called.
I use pyautogui which takes control of your mouse to manually download the book, and I make use pyperclip, which copies and pastes the selected book.
I suggest you dont have anythong important in your clipboard when you run this script.
I'm working with MacOS, when LimeChat is called, I've made it to work with fullscreen. Otherwise, if limechat is in a window, you will have to find
the location of the chatroom #ebook, and the chat bar for this script to work.
The aim is to have the run from a server so it can happen away from your computer and entirely on another computer.
'''

import pyautogui
import subprocess
import time
import pyperclip
import os
import os.path
from os import path
import socket
from threading import Timer

def book_download():

#Opens Limechat and downlods the chosen book through clipboard. Limechat must be full screen and set to automatically join #ebooks on startup.
#DCC transfers must be accepted automatically. To do this, go LimeChat > Preferences > Advanced and set "when recieved a file transfer: accept auto"
#To join #ebooks on startup, go Server > Server Properties > On Login then check the box next to #ebooks.

#The cursor is set to click on #ebooks in the sidebar roughly 1 quarter length of the screen vertically from the bottom right up. This will open #ebooks
#The cursor will then select the chat box "input" bar, where it will then paste the selected book from the main.py script.
#If these locations are different, you will have to change them in the below code. 

    subprocess.call(["/usr/bin/open", "/Applications/LimeChat.app"])
    time.sleep(3)
    pyautogui.click(1200, 590, button = 'left')
    pyautogui.click(100, 635, button = 'left')
    pyautogui.hotkey("command", "v")
    pyautogui.hotkey("return")
    time.sleep(1)
    subprocess.call(["/usr/bin/open", "/Applications/Utilities/Terminal.app"])

def string_check():
	# reutns correct file name for download location
    string = pyperclip.paste()
    return string[string.find(" ")+1:].rstrip()   

def downloading():    
    #does downloading path exist?    
    return path.exists('/users/____________________/downloads/__download__' + string_check()) or path.exists('/users/____________________/downloads/__download__' + string_check().replace(" ","_"))

def downloaded():
    #does downloaded path exist?
	return path.exists('/users/____________________/downloads/' + string_check()) or path.exists('/users/____________________/downloads/' + string_check().replace(" ","_"))

def locate_download():
    #find file if dowloading and return either locating, or downloading
    while downloading() == False and downloaded() == False:
        print("Locating file...")
        time.sleep(5)
        continue
    while downloading() == True:
        print("downloading...")
        time.sleep(3)
        continue
    while downloaded() == True and downloading() == False:
        print("\ndownload complete.\n")
        break        

def rename():
    pyperclip.paste().replace("'","")
    #if downloaded path exists with " ' ", rename to work with calibre call function. cannot take " ' "
    while path.exists("/users/____________________/documents/findle/books/" + string_check()) == True:
        os.rename("/users/____________________/documents/findle/books/" + string_check(), "/users/____________________/documents/findle/Books/" + string_check().replace("'",""))       
        break
    while path.exists('/users/____________________/documents/findle/books/' + string_check().replace(" ","_")) == True:
        os.rename("/users/____________________/documents/findle/books/" + string_check().replace(" ","_"), "/users/____________________/documents/findle/Books/" + string_check().replace("'",""))   
        break

def relocate():
    #if downloaded path exists, relocate file to book folder
    while path.exists("/users/____________________/downloads/" + string_check()) == True:
        os.rename("/users/____________________/downloads/" + string_check(), "/users/____________________/documents/findle/Books/" + string_check())
        print("Relocated \n")    
    while path.exists('/users/____________________/downloads/' + string_check().replace(" ","_")) == True:
        os.rename("/users/____________________/downloads/" + string_check().replace(" ","_"), "/users/____________________/documents/findle/Books/" + string_check().replace(" ","_"))
        print("Relocated \n")
    rename()

def exit_lime():
	#quits lime chat
    time.sleep(1)
    subprocess.call(["/usr/bin/open", "/Applications/LimeChat.app"])
    time.sleep(1)
    pyautogui.hotkey("command", "q")
    pyautogui.hotkey("return")

def time_check():
    folder = "/users/____________________/documents/findle/"
    for file in os.listdir(folder):
        file = file.endswith(".txt")
    if file == False:
        print ("No Files Found. Search again. \n")
        connection.quit()
        main()
    else:
        pass