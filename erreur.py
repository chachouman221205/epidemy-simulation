from tkinter import *

def erreur(titre, message):
    fen = Tk()
    fen.title(titre)
    fen.geometry('400x150')
    Label(text=message).pack(expand=YES)
    fen.mainloop()