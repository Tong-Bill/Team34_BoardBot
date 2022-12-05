from tkinter import *

root = Tk()
root.title('Game Over')
root.geometry('925x500+300+200')
root.configure(bg="#fff") # White Color background
root.resizable(False, False) # Disable window resizing

# Creating frame for Game Over

label = Label(root, bg='white').place(x=110,y=50)
heading = Label(text="Game Over", fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 40, 'bold'))
heading.place(x=200,y=5)













root.mainloop()