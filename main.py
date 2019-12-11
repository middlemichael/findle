'''
Parts of the following script have been written by rocketeer999. https://github.com/Rocketeer999/book-downloader
parts have been taken out and re-worked to work along side with ebook.py and downloader.py
This is my first project with python and first attempt at learning to code. 
The idea started with automating the process of locating books I have downloaded and converting them. 
The idea continued to grow however. Any help is much appreciated. Please use this to only download public domain books.

'''

import pyautogui
import subprocess
import time
import pyperclip
import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
import re
import zipfile
import os
import struct
import sys
import argparse
import shlex
from time import sleep
import jaraco.logging
import six
from six.moves import socketserver
import irc.client
import os
import os.path
from os import path
import download
import ebook
from threading import Timer

nickname = "Scout"

### Uncomment the following 2 lines while commenting out 'filetype =' to be able to choose the filetype. input has to specific though.

#print("select file type. epub, mobi or rar")
#filetype = input()

filetype = 'rar'

def userselect(filename):


#Returns results from search. 
#If you do not wish to search and would like to exit the program, type "q". 
#If you wish to exit your current search and return, type "r". Though This has issues as the first search needs to be closed.
#type "y" to select the file chosen.
#to move through the list, any other character will work, "n" is the correct character to filter, but hitting enter works just as well.



    with zipfile.ZipFile(filename, "r") as z:
        with z.open(z.namelist()[0]) as fin:
            answer = "n"
            for line in fin:
                line = str(line)[2:-5]
                if filetype in line.lower():
                    answer = input(line + " (y/n?)\n")
                if answer == "y":
                	return line.split("::")[0]
                if answer == "r":
                	for file in os.listdir("/users/____________________/documents/findle/"):
                		if file.endswith(".zip"):
                			os.remove(file)
                			main()
                if answer == "q":
                	for file in os.listdir("/users/____________________/documents/findle/"):
                		if file.endswith(".zip"):
                			os.remove(file)
                	quit()
            print("No files found. Search again. \n")
            for file in os.listdir("/users/____________________/documents/findle/"):
                if file.endswith(".zip"):
                    os.remove(file)
            main()


class TestBot(irc.bot.SingleServerIRCBot):
    def __init__(self, searchterm, channel, nickname, server, port=6667):        
        irc.bot.SingleServerIRCBot.__init__(
            self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.searchterm = searchterm
        self.received_bytes = 0
        self.havebook = False
        
    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):        
        c.join(self.channel)
        self.connection.privmsg(self.channel, "@search " + self.searchterm)
        print("Searching ...\n") 
   	#Time check will disconnect the program if no results are found within 15 seconds. Search should return results if there are results within 15seconds.
   	#This is a terrible work around but will do for now. 
        def time_check():
            if not any(file.startswith('SearchBot') for file in os.listdir('/users/____________________/documents/findle/')):
                print("No file found. Unresolved Issue. Program terminates.\n")
                self.connection.quit()
                os._exit(0)       
        t = Timer(15, time_check)
        t.start()
    
    def on_ctcp(self, connection, event):
        payload = event.arguments[1]
        parts = shlex.split(payload)
        if len(parts) != 5: 
            return       
        command, filename, peer_address, peer_port, size = parts
        if command != "SEND":
            return
        self.filename = os.path.basename(filename)
    #if file already exists, overwrite it.    
        if os.path.exists(self.filename):
            print("Overwriting ... \n")
        self.file = open(self.filename, "wb")
        peer_address = irc.client.ip_numstr_to_quad(peer_address)
        peer_port = int(peer_port)
        self.dcc = self.dcc_connect(peer_address, peer_port, "raw")

    def on_dccmsg(self, connection, event):
        data = event.arguments[0]
        self.file.write(data)
        self.received_bytes = self.received_bytes + len(data)    
        self.dcc.send_bytes(struct.pack("!I", self.received_bytes))

    def on_dcc_disconnect(self, connection, event):
        self.file.close()
        print("Returning Results. \n")
        if not self.havebook:
            print("Select file:\n")
            book = userselect(self.filename)
    #Handle the bot !Xon. bot returns resultd with /r----- appended. Delete these characters, and copy only the file name.
            if book.startswith("!Xon"):
                book = book.split("\\r")[0]
            pyperclip.copy(book)
            self.received_bytes = 0             
            self.havebook = True
            os.remove(self.filename)
            self.connection.quit()
            download.book_download()          
            download.locate_download()
            download.relocate()
            download.exit_lime()
    #book has been downloaded and moved to correct folder. process will be repated if prompted "y", or convert will now run "n"/ any character really.
            reply = str(input('Another? (y/n): ')).lower().strip()
            if reply[0] == 'y':
                main()
            else:
                pass
            print("Run convert.\n")
            time.sleep(1)
            ebook.run_convert()
            ebook.send_it()
            self.die()            

def main():

#Search for the book.
#input "c" will cancel the search and go straight to the convert process.
#input "q" will end the program.
#if no nickname is set, you can choose a nickname, doesnt really matter though. scout is currently set.

    global nickname
    searchterm = ""
    if len(sys.argv) == 3:
        searchterm = sys.argv[1]
        nickname = sys.argv[2]
    else:       
        searchterm = input("Search:\n")
        if searchterm == "c":
            print("\nSkip Search. Converting.\n")
            time.sleep(2)
            ebook.run_convert()
            ebook.send_it()
            quit()
        if searchterm == "q":
            quit()
        if nickname == "":
            nickname = input("Enter Nickname:\n")
    server = "irc.irchighway.net"
    port = 6667
    channel = "#ebooks"
    bot = TestBot(searchterm, channel, nickname, server, port)
    bot.start()

#Run the program    
main()
