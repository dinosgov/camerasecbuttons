import cv2
import time 
import datetime
import smtplib
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from email.message import EmailMessage
import winsound
import pywhatkit
from gtts import gTTS
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image
import subprocess
import tkinter as tk
from tkinter import StringVar


root = Tk()
root.title('security')
root.iconbitmap('kitty.ico')


my_img = ImageTk.PhotoImage(Image.open('me.jpg'))
my_Label = Label(image=my_img)
my_Label.pack()


cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

detection = False
detection_stopped_time = None
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5

frame_size = (int(cap.get(3)), int (cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to


 
    user = "Insert your mail"
    password = "insert your password"
    
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(user,password)
    server.send_message(msg)
  


# showinfo, showerror, askquestion, askokcancel, askyesno


if __name__ == "__main__":
    response = messagebox.askyesno('YOU WANT TO BE SAFE','START THE PROGRAMM?')
    #Label(root, text=response).pack()
    if response == 1:
        response2 = messagebox.askyesno('ALERT','Do you want Alert Sound?')
        if response2 == 1:
            sunagermos = 'yes'
        else:
            sunagermos = 'no'

        response3 = messagebox.askyesno('NOTIFICATION','Do you want mail notification?')
        if response3 == 1:
            notification = 'yes'
        else:
            notification = 'no'
            
        while True:
            _, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.2, 3)
            bodies = face_cascade.detectMultiScale(gray, 1.2, 3)
            if len(faces) + len(bodies) > 0:
                if detection:
                    timer_started = False
                else:
                    detection = True
                    current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
                    out = cv2.VideoWriter(f"{current_time}.mp4",fourcc, 20, frame_size)
                    print("Started Recording!")
                    if sunagermos == ("yes"):

                        winsound.PlaySound("alert.wav", winsound.SND_ASYNC | winsound.SND_ALIAS )
                    if notification == ("yes"):
                        email_alert("ALERT", "Open OneDrive", 'the mail that you want to receive the notification')
            elif detection:
                if timer_started:
                    if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                        detection = False
                        timer_started = False
                        out.release()
                        print("Stop Recording!")
                else:
                    timer_started = True
                    detection_stopped_time = time.time()
                    
            
    
            if detection:
                out.write(frame)
        

            #for(x, y, width, height) in bodies:
            #cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 3)

            cv2.imshow("Camera", frame)


            if cv2.waitKey(1) == ord('q'):
                break

        out.release()
        cap.release()
        cv2.destroyAllWindows()
        
    else:
        Label(root, text="GOODBYE").pack()
        quit()
