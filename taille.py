from tkinter import *
from functools import partial
import erreur as erreur

def epurer(c):
    characteres = ["1","2","3","4","5","6","7","8","9","0","."]
    r = ""
    for l in c:
        if l in characteres:
            r += l
    return r

def confirmer(fen_t, xe, ye):

    global x, y
    x, y = int(epurer(xe.get())), int(epurer(ye.get()))

    fen_t.quit()
    return

def nouvelle_taille():
    fen_t = Tk()
    fen_t.title("modification taille")
    fen_t.geometry("400x150")
    
    
    Label(fen_t, text="ATTENTION: Des tailles au dessus de 50 peuvent\ngravement affecter les performances").pack(expand=YES)

    frame = Frame(fen_t)
    
    frame_x = Frame(frame)
    frame_y = Frame(frame)

    xe = Entry(frame_x)
    xe.pack(side=RIGHT)
    ye = Entry(frame_y)
    ye.pack(side=RIGHT)
    
    Label(frame_x, text="x = ").pack(side=LEFT)
    Label(frame_y, text="y = ").pack(side=LEFT)
    
    frame_x.pack()
    frame_y.pack()
    
    confirm = Button(frame, text='confirmer', command=partial(confirmer, fen_t, xe, ye))
    confirm.pack()

    frame.pack(expand=YES)

    fen_t.mainloop()
    fen_t.destroy()

x = 10
y = 10