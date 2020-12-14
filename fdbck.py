from tkinter import *
from functools import partial

def storefeedback(feedback):
    feedback = feedback.get()

    f = open("feedback.txt", "a+")
    f.write(feedback+'\n')
    f.close()

    window.destroy()
    window.quit()

def main_screen():
    global storefeedback
    global window
    
    window = Tk()  
    window.geometry('500x150')
    window.title('Feedback window')
    Label(window, text="SPACE INVADERS", font=('courier', 13), bg='grey', width='500', height='1').pack()
    Label(window, text="").pack()
    feedbacklabel = Label(window, text="Your feedback about the game (you can mention your name if you wish to do so)").pack()
    feedback = StringVar()
    feedbackentry = Entry(window, textvariable=feedback, width='81', xscrollcommand=True).pack()
    
    storefeedback = partial(storefeedback, feedback)
    
    Label(window, text="").pack()
    Button(window, text="Submit", command=storefeedback).pack()

    window.mainloop()
