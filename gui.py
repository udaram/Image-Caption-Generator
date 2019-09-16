from tkinter import*
from PIL import Image, ImageTk
from tkinter import filedialog
from shutil import copyfile
import gui_sub 
global filedest
def choosephoto():
    #root.destroy()
    filedest=filedialog.askopenfilename(initialdir="images",title="Select Photo",filetypes=(("jpeg files","*.jpeg",),(".jpg files","*.jpg")))
    gui_sub.main(filedest,root)
def quitgui():
    root.destroy()
global root
root=Tk()
root.title("Image Caption Generator")
#root.geometry("500x500")

f1=Frame(root,bg="grey",borderwidth=6,relief=GROOVE)
f1.pack(side=TOP,fill=X)
f2=Frame(root,bg="grey",borderwidth=6,relief=GROOVE)
f2.pack(side=TOP,fill=X)
Label(f1,text="Welcome to Image Caption Generator",fg="red",bg="Green",font="Helvetica 16 bold").pack()
img=Image.open("index.jpeg")
defaultphoto=ImageTk.PhotoImage(img)
l1=Label(f2,image=defaultphoto)
l1.pack()
btn1=Button(root,text="Choose Photo",command=choosephoto,height=2,width=20,bg='blue',font="Helvetica 16 bold",pady=10)
btn1.pack() 

Button(root,text="Quit",command=quitgui,height=2,width=20,bg='violet',font="Helvetica 16 bold",pady=10).pack()

root.mainloop() 