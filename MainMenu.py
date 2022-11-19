from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

# Sample settings Screen
root = Tk()
root.title('Main Menu')
root.geometry('925x500+300+200')
root.configure(bg="#fff") # White Color background
root.resizable(False, False) # Disable window resizing

# Initiated a new game
def newGame():
    newWindow = Toplevel(root)
    newWindow.title("Please wait")
    newWindow.geometry('300x125')
    def cancel():
        newWindow.destroy()

    progressLabel = Label(newWindow, text="Baxter is scanning the board...", fg='black', border=0)
    progressLabel.place(x=70,y=50)
    progress = ttk.Progressbar(newWindow, orient=HORIZONTAL, mode='determinate')       
    progress.pack(pady=25)
    progress.start(10)
  # Cancel Button
    cancelButton = Button(newWindow, text="Cancel", font=('Microsoft YaHei UI Light', 14, 'bold'), command=cancel)
    cancelButton.pack()

# Opening images
image5 = Image.open('image5.png')
image5.thumbnail((398,200))
mainMenuImage = ImageTk.PhotoImage(image5)

image6 = Image.open('image6.png')
image6.thumbnail((100,100))
mainMenuImage2 = ImageTk.PhotoImage(image6)

image7 = Image.open('image7.png')
image7.thumbnail((200,200))
mainMenuImage3 = ImageTk.PhotoImage(image7)

# Creating frame for menu options
settingsFrame = Frame(root, width=350, height=390, bg='white')
settingsFrame.place(x=480,y=70)
label = Label(root, image=mainMenuImage, bg='white').place(x=50,y=150)
label2 = Label(root, image=mainMenuImage2, bg='white').place(x=740,y=40)
label3 = Label(root, image=mainMenuImage3, bg='white').place(x=100,y=33)
heading = Label(settingsFrame, text="Main Menu", fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=85,y=5)

Button(settingsFrame, width=39, pady=7, text='New Game', bg='#57a1f8', fg='white', border=0, command=newGame).place(x=35,y=80)
Button(settingsFrame, width=39, pady=7, text='Saved Logs', bg='#57a1f8', fg='white', border=0).place(x=35,y=130)
Button(settingsFrame, width=39, pady=7, text='Game Rules', bg='#57a1f8', fg='white', border=0).place(x=35,y=180)
Button(settingsFrame, width=39, pady=7, text='Settings', bg='#57a1f8', fg='white', border=0).place(x=35,y=230)
Button(settingsFrame, width=18, pady=7, text='Logout', bg='#57a1f8', fg='white', border=0).place(x=35,y=290)
Button(settingsFrame, width=18, pady=7, text='Quit', bg='#57a1f8', fg='white', border=0).place(x=185,y=290)
root.mainloop()