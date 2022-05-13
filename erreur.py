from tkinter import *

def erreur(titre, message):
    fen = Tk()
    fen.title(titre)
    fen.geometry('300x150')
    Label(fen, text=message).place(x=5,y=5)
    Button(fen, text="ok", command=fen.destroy).place(x=265,y=120,width=30)
    fen.mainloop()
    return