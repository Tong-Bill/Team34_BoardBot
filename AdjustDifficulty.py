from tkinter import *
from PIL import ImageTk, Image

# Sample settings Screen
root = Tk()
root.title('Settings')
root.geometry('925x500+300+200')
root.configure(bg="#fff") # White Color background
root.resizable(False, False) # Disable window resizing

# Subsetting
def difficulty():
    newWindow = Toplevel(root)
    newWindow.title("Level")
    newWindow.geometry('200x200')

    # Slider for difficulty mode
    slider = Scale(newWindow, from_=1, to=3, orient="horizontal")
    slider.grid(row=1,column=0,columnspan=2,pady=10)
    slider.pack()
    # Save Button
    saveButton = Button(newWindow, text="Save", font=("Arial", 14))
    saveButton.pack()

# Opening images
image3 = Image.open('image3.png')
image3.thumbnail((398,332))
settingsImage = ImageTk.PhotoImage(image3)

image4 = Image.open('image4.png')
image4.thumbnail((100,100))
settingsImage2 = ImageTk.PhotoImage(image4)

# Creating frame for Settings
settingsFrame = Frame(root, width=350, height=390, bg='white')
settingsFrame.place(x=480,y=70)
label = Label(root, image=settingsImage, bg='white').place(x=50,y=50)
label2 = Label(root, image=settingsImage2, bg='white').place(x=740,y=40)
heading = Label(settingsFrame, text="Settings", fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=100,y=5)

Button(settingsFrame, width=39, pady=7, text='Adjust Difficulty', bg='#57a1f8', fg='white', border=0, command=difficulty).place(x=35,y=80)
Button(settingsFrame, width=39, pady=7, text='Adjust Display', bg='#57a1f8', fg='white', border=0).place(x=35,y=130)
Button(settingsFrame, width=39, pady=7, text='Manual Mode', bg='#57a1f8', fg='white', border=0).place(x=35,y=180)
Button(settingsFrame, width=39, pady=7, text='System Information', bg='#57a1f8', fg='white', border=0).place(x=35,y=230)
Button(settingsFrame, width=20, pady=7, text='Back', bg='#57a1f8', fg='white', border=0).place(x=100,y=290)
root.mainloop()