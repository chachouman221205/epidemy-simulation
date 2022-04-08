from tkinter import *
from functools import partial

def confirmer(fen, infection, recuperation_min, recuperation_max, mortalite):
    infection = infection.get()
    recuperation_min = recuperation_min.get()
    recuperation_max = recuperation_max.get()
    mortalite = mortalite.get()

    global R

    if infection == 0:
        infection = 0.1
    if recuperation_max < recuperation_min:
        return False
        
    R = {"nb_voisins":infection, "recup_min": recuperation_min, "recup_max":recuperation_max, "proba_mort":mortalite}
    
    fen.destroy()

def nouvelle_regle():
    fen = Tk()
    fen.title('Paramètres')
    infection = Scale(fen, orient='horizontal', from_=0,to=8, resolution=0.1, tickinterval=0.5, length=350, label="Nombre minimum de voisin pour être infecté")
    infection.pack()
    recuperation_min = Scale(fen, orient='horizontal', from_=0,to=10, resolution=0.1, tickinterval=1, length=350, label="Nombre minimum de jours pour être soigné")
    recuperation_min.pack()
    recuperation_max = Scale(fen, orient='horizontal', from_=0,to=10, resolution=0.1, tickinterval=1, length=350, label="Nombre maximum de jours pour être soigné")
    recuperation_max.pack()
    mortalite = Scale(fen, orient='horizontal', from_=0,to=1, resolution=0.01, tickinterval=0.25, length=350, label="Chance de mourir du virus chaque jour")
    mortalite.pack()

    confirm = Button(fen, text='confirmer', command=partial(confirmer, fen, infection, recuperation_min, recuperation_max, mortalite))
    confirm.pack()
    
    fen.mainloop()