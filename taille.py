from tkinter import *
from functools import partial
import erreur as erreur

def epurer(c):
    characteres = ["1","2","3","4","5","6","7","8","9","0"]
    r = ""
    for l in c:
        if l in characteres:
            r += l
    return r

def confirmer(fen, xe, ye):

    x_ = int(epurer(xe.get()))
    y_ = int(epurer(ye.get()))

    if x_ <= 0 or y_ <= 0:
        erreur.erreur("ERREUR: entrée non valide", "la taille de la grille doit être strictement posisitive")
        return

    global x, y
    x, y = x_, y_

    fen.destroy()

def nouvelle_taille():
    fen = Tk()
    fen.title("modification taille")
    fen.geometry("400x150")

    frame = Frame(fen)

    xe = Entry(frame)
    xe.insert(0, "x = ")
    xe.pack()
    ye = Entry(frame)
    ye.insert(0, "y = ")
    ye.pack()
    confirm = Button(frame, text='confirmer', command=partial(confirmer, fen, xe, ye))
    confirm.pack()

    frame.pack(expand=YES)

    fen.mainloop()
    global x, y
    print(x, y)

x = 10
y = 10