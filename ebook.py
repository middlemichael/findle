'''
This is my first Python code. It's not the prettiest, but it works. ...mostly...
It is structured to my computer, MacOS, so some tweaking will need to be done in order for it work for you.
if you have any comments please let me know. I would love to hear ways I can improve.

'''

import subprocess
import os
from pathlib import Path

#folder where the books are found
folder = "/Users/____________________/Documents/findle/Books/"

def book_shelf():
	
#Finds the number of books stored. If 0 books, the conversion will not run and program will end.
#Books are files ending with .epub, .rar, .mobi, .pdf, and .html
#More books can be recognized by copying the code "elif filename...." and changing the extension to what fits.

    books = []
    for filename in os.listdir(folder):
        if filename.endswith(".epub"):
            epub = filename[:-len(".epub")]
            books.append(epub)
        elif filename.endswith(".rar"):
            rar = filename[:-len(".rar")]
            books.append(rar)
        elif filename.endswith(".mobi"):
            os.rename(folder + filename, folder + "Kindle/" + filename)
            print ("Moved" + filename )
        elif filename.endswith(".pdf"):
            pdf = filename[:-len(".pdf")]
            books.append(pdf)
        elif filename.endswith(".html"):
            html = filename[:-len(".html")]
            books.append(html)
        else:
            pass            
    return len(books)
    

def book():
#Returns the name of one book in folder that will be processed for conversion.
    files = []
    for filename in os.listdir(folder):
        if filename.endswith(".epub"):
            epub = filename
            files.append(epub)           
        elif filename.endswith(".rar"):
            rar = filename
            files.append(rar)           
        elif filename.endswith(".mobi"):
            mobi = filename
            files.append(mobi)
        elif filename.endswith(".pdf"):
            pdf = filename
            files.append(pdf)
        elif filename.endswith(".html"):
            html = filename
            files.append(html)
    while len(files) > 0:
        return files[0]
    else:
        files = "Empty"
        return files


def convert():
#Converts the chosen book to the correct file, deletes the orignal file and places the now .mobi file into a subfolder.
#The book is now ready to be sent
    call = '/Applications/calibre.app/Contents/MacOS/ebook-convert '   
    folder_out = folder + ("Kindle/")  
    for files in book():
        if book() == "Empty":
            return book()
        else:
            book_in = folder + book()
            book_out = folder + "Kindle/" + book()[:-4] + (".mobi")
            final = call + " '" + book_in + "' '" + book_out + "' "
            os.system(final)   
            print("\n", book(),"Converted\n")
            os.remove(book_in)

def run_convert():
#Loops the convert process until there are no more books to convert.
    while book_shelf() > 0:
        convert()
        continue
        if book_shelf() == 0:
            break
    else:
        print("Sending Files to Kindle. \n")



def first_send():
#Returns a book ready to be sent, if there is no book, returns nothing.
    send = []
    for mobi in os.listdir(folder + "Kindle/"):
        if mobi.endswith(".mobi"):
            send.append(mobi)
        else:
            pass
    for file in os.listdir(folder + "Kindle/"):
        if file != file.endswith(".mobi"):
            send.append("No Mobis Found")          
    return send[0]


def send_to_kindle():
#Packages book to email and sends

    print("Sending " + first_send())
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders
    import os.path
    email = '____________________y@gmail.com'
    password = '____________________'
    send_to_email = "____________________@kindle.com"
    subject = first_send()
    message = first_send() + (" Sent to Kindle")
    file_location = '/users/____________________/documents/findle/books/kindle/' + first_send()
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    # Setup the attachment
    filename = os.path.basename(file_location)
    attachment = open(file_location, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    # Attach the attachment to the MIMEMultipart object
    msg.attach(part)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, send_to_email, text)
    server.quit()   
    print("Sent\n")
    #Remove file from folder
    os.remove(file_location)


def booklist():
#Returns value of books to send. if value = 0, will not send anything
    shelf = []
    for filename in os.listdir(folder + "Kindle/"):
        if filename.endswith(".mobi"):
            mobi = filename[:-len(".mobi")]
            shelf.append(mobi)
        else:
            pass        
    return len(shelf)


def send_it():
#if there are books to send, the process will loop until all are sent.
    while booklist() > 0:
        send_to_kindle()
        continue
        if booklist() == 0:
            break
    else:
    	pass



