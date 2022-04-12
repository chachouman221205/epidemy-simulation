from tkinter import *

def erreur(titre, message):
    fen = Tk()
    fen.title(titre)
    fen.geometry('400x150')
    Label(text=message).grid(row=2,column=2)
    fen.mainloop()
