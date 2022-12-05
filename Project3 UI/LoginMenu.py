from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

# Sample Sign In screen
root = Tk()
root.title('Login')
root.geometry('925x500+300+200')
root.configure(bg="#fff") # White Color background
root.resizable(False, False) # Disable window resizing

def signIn():
    username = user.get()
    password = key.get()
    if username == 'bill' and password == 'team34':
        screen = Toplevel(root)
        screen.title("App")
        screen.geometry('925x500+300+200')
        screen.config(bg='white')
        Label(screen, text='Hello Everyone!', bg='#fff', font=('Calibri(Body)', 50, 'bold')).pack(expand=True)
        screen.mainloop()
    elif username != 'bill' and password != 'team34':
        messagebox.showerror("Error", "Invalid username or password")
    elif password != "team34":
        messagebox.showerror("Error", "Invalid username or password")
    elif username != "bill":
        messagebox.showerror("Error", "uInvalid username or password")

# Opening image 
image1 = Image.open('image1.png')
image1.thumbnail((398,332))
loginImage = ImageTk.PhotoImage(image1)
# Creating frame for login
loginFrame = Frame(root, width=350, height=350, bg='white')
loginFrame.place(x=480,y=70)
label = Label(root, image=loginImage, bg='white').place(x=110,y=50)
heading = Label(loginFrame, text="Sign in", fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=100,y=5)

# Username Box
def focusEnter(e):
    user.delete(0, 'end')
def focusLeave(e):
    name=user.get()
    if name=='':
        user.insert(0, 'Username')

user = Entry(loginFrame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11) )
user.place(x=30,y=80)
user.insert(0, "Username")
user.bind('<FocusIn>', focusEnter)
user.bind('<FocusOut>', focusLeave)
Frame(loginFrame, width=295, height=2, bg='black').place(x=25,y=107)

# Password Box
def focusEnter(e):
    key.delete(0, 'end')
def focusLeave(e):
    name=user.get()
    if name=='':
        key.insert(0, 'Password')

key = Entry(loginFrame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11) )
key.place(x=30,y=150)
key.insert(0, "Password")
key.bind('<FocusIn>', focusEnter)
key.bind('<FocusOut>', focusLeave)
Frame(loginFrame, width=295, height=2, bg='black').place(x=25,y=177)

# Login Button
Button(loginFrame, width=39, pady=7, text='Login', bg='#57a1f8', fg='white', border=0, command=signIn).place(x=35,y=204)
label = Label(loginFrame, text="Don't have an account?", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
label.place(x=75,y=270)
# Sign Up Button
signUp = Button(loginFrame, width=6, text="Sign up", border=0, bg='white', fg='#57a1f8', cursor='hand2')
signUp.place(x=215,y=270)

root.mainloop()