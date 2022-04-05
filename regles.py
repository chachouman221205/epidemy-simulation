from tkinter import *
from functools import partial

def confirmer(fen, infection, recuperation_min, recuperation_max):
    global R
    if recuperation_max < recuperation_min:
        return False
    fen.destroy()
    R = [infection, recuperation_min, recuperation_max]
    print(R)

def nouvelle_regle():
    fen = Tk()
    infection = Scale(fen, orient='horizontal', from_=0.1,to=8, resolution=0.1, tickinterval=0.5, length=350, label="Nombre minimum de voisin pour être infecté")
    infection.pack()
    recuperation_min = Scale(fen, orient='horizontal', from_=0,to=10, resolution=0.1, tickinterval=1, length=350, label="Nombre minimum de jours pour être soigné")
    recuperation_min.pack()
    recuperation_max = Scale(fen, orient='horizontal', from_=0,to=10, resolution=0.1, tickinterval=1, length=350, label="Nombre maximum de jours pour être soigné")
    recuperation_max.pack()

    confirm = Button(fen, text='confirmer', command=partial(confirmer, fen, infection.get(), recuperation_min.get(), recuperation_max.get()))
    confirm.pack()
    
    fen.mainloop()