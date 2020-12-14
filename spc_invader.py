import gamecode
from tkinter import *
from functools import partial

def pycode(uname):
    gamecode.play(uname)

def validateLogin(username):
    global uname
    
    uname = username.get()
    try:
        win.destroy()
        win.quit()
        pycode(uname)
    except Exception:
        pass
    
def main_screen():
    global validateLogin
    global win
    
    win = Tk()  
    win.geometry('400x150')  
    win.title('Home')

    Label(win, text="SPACE INVADERS", font=('courier', 13), bg='grey', width='400', height='1').pack()
    Label(win, text="").pack()
    usernameLabel = Label(win, text="Username*").pack()
    username = StringVar()
    usernameEntry = Entry(win, textvariable=username).pack()  

    validateLogin = partial(validateLogin, username)
    
    Label(win, text="").pack()
    playButton = Button(win, text="Play", command=validateLogin).pack()

    win.mainloop()

main_screen()
