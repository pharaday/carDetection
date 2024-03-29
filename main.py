import sys
import os
import tkinter

try:
    import Tkinter as tk
except ImportError:                   # to prevent version issues
    import tkinter as tk
try:
    import ttk
except ImportError:
    import tkinter.ttk as ttk
try:
    from tkinter import messagebox
except:
    # Python 2
    import tkMessageBox as messagebox

from PIL import ImageTk, Image
from tkinter import filedialog   # we will use this for getting images from any direction
import os
#import MyModel
#import cv2

# Main Window 
root = tk.Tk()
root.title("Anyqta")
root.geometry("800x650+150+125")
root.config(bg="white")



### FUNCTIONS

# Message boxes for giving information to the user
def noPhotoSelected():
   tkinter.messagebox.showinfo( "Warning! ", "Please upload a photo via ** Upload Photo ** button ! ")

# we hide / show our buttons for better user experience
def showTheNextButton():
    nextButton.place(relx = 0.67, rely=0.05 ,relwidth=0.3, relheight=0.45)
def showThePreviousButton():
    previousButton.place(relx = 0.03, rely=0.05 ,relwidth=0.3, relheight=0.45)


# make sure that user really want to exit from our app
def areYouSure():
    exitKontrol = messagebox.askquestion("Exit","Are you sure?")
    if exitKontrol == 'yes':
        quit()


### this function is important
# we show images but We resize the images based on main window size!
def showTheImages():
    resized = Image.open(str(filepath[thePhotoWeWorkingOn]))
    maxsize = (photoPanel.winfo_width() - 50,photoPanel.winfo_height() - 50 )
    resized.thumbnail(maxsize, Image.ANTIALIAS)
    img = ImageTk.PhotoImage(resized)
    photoPanel.config(image = img)
    photoPanel.image = img

### Button functions

def openfn():
    global filepath  # file path for the photos
    global thePhotoWeWorkingOn
    thePhotoWeWorkingOn = 0  # this is because we wanna take the first photo
    filepath = filedialog.askopenfilenames(title='Please select a photo for detection')
    global photo_selected
    photo_selected = 1
    # we have 2 options here -> askopenfile -> askopenfiles.
    # we prefer askopenfiles because we want to work on multiple images
    showTheImages()

    print(len(filepath))
    if len(filepath) == 1:
        nextButton.place_forget()
        previousButton.place_forget()
    else:
        showTheNextButton()


# go to the next image
def next():
    showThePreviousButton()
    global thePhotoWeWorkingOn
    if thePhotoWeWorkingOn == len(filepath) - 2:
        thePhotoWeWorkingOn = thePhotoWeWorkingOn + 1
        showTheImages()
        nextButton.place_forget()
        return
    elif thePhotoWeWorkingOn < len(filepath) - 1:
        thePhotoWeWorkingOn = thePhotoWeWorkingOn + 1
        showTheImages()


# go to the previous image
def previous():
    showTheNextButton()
    global thePhotoWeWorkingOn
    if thePhotoWeWorkingOn == 1:
        thePhotoWeWorkingOn = thePhotoWeWorkingOn - 1
        showTheImages()
        previousButton.place_forget()
        showTheNextButton()
        return
    else:
        thePhotoWeWorkingOn = thePhotoWeWorkingOn - 1
        showTheImages()
        showTheNextButton()


# calling the model and then show the detected image

def open_img():
    if photo_selected == 1:
        MyModel.detect_objects(str(filepath[thePhotoWeWorkingOn]), SCORE_THRESHOLD)
        resized = Image.open('imgWeWorkingOn/temp.jpg')
        maxsize = (photoPanel.winfo_width() - 50, photoPanel.winfo_height() - 50)
        resized.thumbnail(maxsize, Image.ANTIALIAS)
        img = ImageTk.PhotoImage(resized)
        photoPanel.config(image=img)
        photoPanel.image = img
    else:
        noPhotoSelected()



# The frame which has the buttons

# Definition of the label and a frame definition for this label.
framePhoto = tk.Frame(root, bg="#d0dbc1")
framePhoto.place(relheight=0.6, relwidth=0.8, relx=0.1,rely=0.1)
photoPanel = tk.Label(framePhoto, bg="#5d46e2", text="Фото")
photoPanel.place( relheight=1, relwidth=1,)
photoPanel.configure(highlightcolor="black")
photoPanel.configure(activeforeground="black")

frameD = tk.Frame(root, bg="#d5d9e3")
frameD.place(relheight=0.18, relwidth=0.8, relx=0.1,rely=0.8)

############################### Button Operations ###################
# Previous Button
previousButton = tk.Button(frameD,fg='red', text ="Previous", command= previous)

#ımage Upload Button
uploadImage = tk.Button(frameD,fg='purple', text ="Загрузить изображение", command= openfn)
uploadImage.place(relx = 0.35, rely=0.05 ,relwidth=0.3, relheight=0.45)

# Next Button
nextButton = tk.Button(frameD,fg='red', text ="Next", command= next)

# The detection button
detectButton = tk.Button(frameD,fg='green', text ="Детектировать", command= open_img)
detectButton.place(relx = 0.35, rely=0.5 ,relwidth=0.3, relheight=0.45)

# The exit button at the top-left
exitButton = tk.Button(root , bg="gray", text="Выход", command= areYouSure)
exitButton.place(relx=0.85, rely=0, relheight=0.05, relwidth=0.05)


def quit():
    root.destroy()






root.mainloop()