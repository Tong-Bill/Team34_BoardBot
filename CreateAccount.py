from tkinter import * 
from tkinter import messagebox
from PIL import ImageTk, Image

# Sample Sign Up screen
root = Tk()
root.title('Sign Up')
root.geometry('925x500+300+200')
root.configure(bg="#fff") # White Color background
root.resizable(False, False) # Disable window resizing

# To be connected to database in the future
def signUp():
    pass

def haveAccount():
    root.destroy()

# Opening image 
image2 = Image.open('image2.png')
image2.thumbnail((398,332))
createAccountImage = ImageTk.PhotoImage(image2)
# Creating frame for create account
createAccountFrame = Frame(root, width=350, height=390, bg='white')
createAccountFrame.place(x=480,y=70)
label = Label(root, image=createAccountImage, bg='white').place(x=50,y=50)
heading = Label(createAccountFrame, text="Sign Up", fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=100,y=5)

# Username Box
def focusEnter(e):
    user.delete(0, 'end')
def focusLeave(e):
    name=user.get()
    if name=='':
        user.insert(0, 'Username')

user = Entry(createAccountFrame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11) )
user.place(x=30,y=80)
user.insert(0, "Username")
user.bind('<FocusIn>', focusEnter)
user.bind('<FocusOut>', focusLeave)
Frame(createAccountFrame, width=295, height=2, bg='black').place(x=25,y=107)

# Password Box
def focusEnter(e):
    key.delete(0, 'end')
def focusLeave(e):
    name=user.get()
    if name=='':
        key.insert(0, 'Password')

key = Entry(createAccountFrame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11) )
key.place(x=30,y=130)
key.insert(0, "Password")
key.bind('<FocusIn>', focusEnter)
key.bind('<FocusOut>', focusLeave)
Frame(createAccountFrame, width=295, height=2, bg='black').place(x=25,y=157)

# Confirm Password Box
def focusEnter(e):
    confirmkey.delete(0, 'end')
def focusLeave(e):
    name=user.get()
    if name=='':
        confirmkey.insert(0, 'Password')

confirmkey = Entry(createAccountFrame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11) )
confirmkey.place(x=30,y=180) # y = 157 + 23
confirmkey.insert(0, "Confirm Password")
confirmkey.bind('<FocusIn>', focusEnter)
confirmkey.bind('<FocusOut>', focusLeave)
Frame(createAccountFrame, width=295, height=2, bg='black').place(x=25,y=207) # y = 180 + 27

# Email Box
def focusEnter(e):
    email.delete(0, 'end')
def focusLeave(e):
    name=user.get()
    if name=='':
        email.insert(0, 'Email')

email = Entry(createAccountFrame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11) )
email.place(x=30,y=230)
email.insert(0, "Email")
email.bind('<FocusIn>', focusEnter)
email.bind('<FocusOut>', focusLeave)
Frame(createAccountFrame, width=295, height=2, bg='black').place(x=25,y=257)

# Special Code Box
def focusEnter(e):
    code.delete(0, 'end')
def focusLeave(e):
    name=user.get()
    if name=='':
        code.insert(0, 'Invite Code')

code = Entry(createAccountFrame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11) )
code.place(x=30,y=280)
code.insert(0, "Invite Code")
code.bind('<FocusIn>', focusEnter)
code.bind('<FocusOut>', focusLeave)
Frame(createAccountFrame, width=295, height=2, bg='black').place(x=25,y=307)

# Sign up Button
Button(createAccountFrame, width=39, pady=7, text='Sign up', bg='#57a1f8', fg='white', border=0).place(x=35,y=330)
label = Label(createAccountFrame, text="I already have an account", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
label.place(x=75,y=370) # + 120y
# Sign In button
signIn = Button(createAccountFrame, width=6, text="Sign in", border=0, bg='white', fg='#57a1f8', cursor='hand2', command=haveAccount)
signIn.place(x=220,y=370)

root.mainloop()