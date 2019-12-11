# findle

In order for this to work you will need to make a few changes and download a few packages and programs.

you will need to have an IRC client running. For this, I am using LimeChat for MacOS
https://itunes.apple.com/us/app/limechat/id414030210?mt=12
you will need to install calibre
https://calibre-ebook.com

and you will need to install the following packages:

pyautogui
https://pyautogui.readthedocs.io/en/latest/
irc
https://github.com/jaraco/irc
pyperclip
https://pypi.org/project/pyperclip/

Packages can be installed by $ pip3 install -packagename-

You will also need to have a gmail account that the script can have access to. read here.
https://realpython.com/python-send-email/#option-1-setting-up-a-gmail-account-for-development
in the ebook.py file, you will see where to put your email and password, as well as your kindle address.

This folder should live at /users/yourname/documents/findle for this to work. you will need to go through the code and replace all ____________ with your username. Please make sure to read the comments in each file as well. You may run into a few issues working with pyautogui as I've set it to work when limechat is fullscreen. in order to connect to Ebooks IRC, i suggest to read this.
https://www.reddit.com/r/Piracy/comments/2oftbu/guide_the_idiot_proof_guide_to_downloading_ebooks/

This is my first project, please leave feedback if you feel I can improve or you yourself know how to improve the project.
Please only download public domain books.
many thanks to all those who have developed the packages, programs and snippets of code I have used in this project.

to run the script.
$ cd /users/yourname/documents/findle
$ pyhton main.py
