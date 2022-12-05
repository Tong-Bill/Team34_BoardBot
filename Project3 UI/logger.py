import logging
from tkinter import *

# Sample logger during a game

# Creating a logger
logging.basicConfig(filename="logger.txt", format='%(asctime)s %(message)s', filemode='w')
# Creating an object & setting logger level
logger = logging.getLogger()
logger.setLevel(logging.INFO)
 
# Example logging messages
logger.info("Successfully executed ACTION 1")
logger.info("Successfully executed ACTION 2")
logger.info("Successfully executed ACTION 3")
logger.info("Successfully executed ACTION 4")
logger.info("Successfully executed ACTION 5")

# The root of the application
root = Tk()
root.title("Game In Progress") # Sets window name
root.geometry('440x440') # Sets width x height of window
root.configure(bg='#333333') # Sets background color

# Creates a box to write the information
infoBox = Text(root, font=("Arial", 12))

# Opens & reads the info from logger.txt
textFile = open("logger.txt", "r")
log = textFile.read()
infoBox.insert(END, log)
textFile.close()
infoBox.pack()

# Loop is required for interface to function
root.mainloop()