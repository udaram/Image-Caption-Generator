from tkinter import*
from PIL import Image, ImageTk
import GreedyCaption
import beamsearch

def quitfrom():
    #quit()
    screen.destroy()

def greedycaption():
    caption=GreedyCaption.generate_caption(filepath)
    caption="Greedy Caption:   "+caption 
    label.config(text=caption,fg='violet',bg='green',font="Helvetica 16 bold")
    label.update_idletasks()

def beamcaption():
    caption=beamsearch.generate_caption(filepath)
    caption="Beamsearch Caption:"+caption 
    label.config(text=caption,fg='violet',bg='green',font="Helvetica 16 bold")
    label.update_idletasks()

def main(file,root):
    global filepath
    global screen
    filepath=file
    screen=Toplevel(root)
    screen.title("Image Caption Generator")
    ff1=Frame(screen,bg="grey",borderwidth=6,relief=GROOVE)
    ff1.pack(side=TOP,fill=X)
    ff2=Frame(screen,bg="grey",borderwidth=6,relief=GROOVE)
    ff2.pack(side=TOP,fill=X)
    
    global ff4
    global label 
    ff4=Frame(screen,bg="grey",borderwidth=6,relief=GROOVE)
    ff4.pack(side=TOP,fill=X)
    ff3=Frame(screen,bg="grey",borderwidth=6,relief=GROOVE)
    ff3.pack(side=TOP,fill=X)
    Label(ff1,text="Welcome to Image Caption Generator",fg="red",bg="Green",font="Helvetica 16 bold").pack()
    img=Image.open(file)
    img=img.resize((500,400))
    photo=ImageTk.PhotoImage(img)
    Label(ff2,image=photo).pack() 
    label=Label(ff4,text="Caption",fg="blue",bg="gray",font="Helvetica 16 bold")
    label.pack()
    Button(ff3,text="Greedy Search Caption",bg="yellow",command=greedycaption,height=2,width=20,font="Helvetica 16 bold").pack(side=LEFT)
    Button(ff3,text="Beam Search Caption",bg="violet",command=beamcaption,height=2,width=20,font="Helvetica 16 bold").pack(side=LEFT)
    Button(ff3,text='Quit',bg="red",command= quitfrom,height=2,width=20,font="Helvetica 16 bold").pack()
    screen.mainloop()


#main('/home/udaram/Desktop/Image Captioning/images/image1.jpeg')
