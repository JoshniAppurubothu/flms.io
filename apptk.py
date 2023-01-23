import tkinter 
from tkinter import *
from tkinter.font import Font
from tkinter import ttk
import PIL
import PIL.Image as p
from PIL import Image,ImageTk
root=Tk()
root.title("Leave Management System")
root.wm_attributes('-fullscreen', '1')
path1="sdmlogo.jpg"
path2="SDMSMK.jpg"
img = ImageTk.PhotoImage(p.open(path1))
img2 = ImageTk.PhotoImage(p.open(path2))
label1=Label(image=img)
label2=Label(image=img)
label1.pack()
label2.pack()
root.mainloop()
