from tkinter import *
from functools import partial
import erreur

def confirmer(fen, infection, recuperation_min, recuperation_max, mortalite, oubli,vaccin):
    infection = 8-infection.get()
    recuperation_min = int(recuperation_min.get())
    recuperation_max = int(recuperation_max.get())
    mortalite = mortalite.get()
    oubli = oubli.get()
    vaccin = vaccin.get()

    global R

    if infection == 0:
        infection = 0.1
    if recuperation_max < recuperation_min:
        erreur.erreur("problème de règle", "ATTENTION: Le temps de récupération maximum doit être supérieur au temps de récupération minimum")
        
    R = {"nb_voisins":infection,
    "recup_min": recuperation_min,
    "recup_max":recuperation_max,
    "proba_mort":mortalite,
    "proba_oubli":oubli,
    "proba_vaccination":vaccin
    }
    
    fen.quit()

def nouvelle_regle():
    fen = Tk()
    infection = Scale(fen, orient='horizontal', from_=0,to=8, resolution=0.1, tickinterval=0.5, length=350, label="Infectuosité")
    infection.pack()
    recuperation_min = Scale(fen, orient='horizontal', from_=0,to=10, resolution=1, tickinterval=1, length=350, label="Nombre minimum de jours pour être soigné")
    recuperation_min.pack()
    recuperation_max = Scale(fen, orient='horizontal', from_=0,to=10, resolution=1, tickinterval=1, length=350, label="Nombre maximum de jours pour être soigné")
    recuperation_max.pack()
    mortalite = Scale(fen, orient='horizontal', from_=0,to=1, resolution=0.01, tickinterval=0.25, length=350, label="Mortalité du virus")
    mortalite.pack()
    oubli = Scale(fen, orient='horizontal', from_=0,to=1, resolution=0.01, tickinterval=0.25, length=350, label="Probabilité de perdre les défenses immunitaires")
    oubli.pack()
    vaccin = Scale(fen, orient='horizontal', from_=0,to=1, resolution=0.01, tickinterval=0.25, length=350, label="Probabilité qu'une case se vaccine")
    vaccin.pack()

    confirm = Button(fen, text='confirmer', command=partial(confirmer, fen, infection, recuperation_min, recuperation_max, mortalite, oubli, vaccin))
    confirm.pack()
    
    fen.mainloop()
    fen.destroy()

R = {}
