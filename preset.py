from tkinter import *
from functools import partial
import erreur as erreur

def confirmer(fen_l, nom_):

    try:
        f = open(f"saves/{nom_.get()}.txt")
    except FileNotFoundError:
        erreur.erreur("Fichier introuvable", "vérifiez le nom de la sauvegarde et rééssayez")
        return

    global file
    file = f

    fen_l.quit()
    return

def ouvrir():
    fen_l = Tk()
    fen_l.title("charger une sauvgarde")
    fen_l.geometry("400x150")
    
    frame = Frame(fen_l)
    frame2 = Frame(frame)

    Label(frame2, text="nom de la sauvegarde: ").pack(side=LEFT)
    nom = Entry(frame2)
    nom.pack(expand=YES,side=RIGHT)
    
    frame2.pack(side=TOP)
    
    confirm = Button(frame, text='confirmer', command=partial(confirmer, fen_l, nom))
    confirm.pack(side=BOTTOM)

    frame.pack(expand=YES)

    fen_l.mainloop()
    fen_l.destroy()

def confirmer2(fen_s, nom_, grille):
    resultat = ""
    for y in grille:
        for x in y:
            resultat += str(x) + ","
        resultat = resultat[0:-1] + ";"
    resultat = resultat[0:-1]
    import os
    try:
        open(f"saves/{nom_.get()}.txt", "x")
    except FileExistsError as err:
        erreur.erreur("sauvegarde existante", "Une sauvegarde éxiste déjà sous ce nom.")
    open(f"saves/{nom_.get()}.txt", "w").write(resultat)
    fen_s.quit()
    return

def save(grille):
    fen_s = Tk()
    fen_s.title("sauvegarder la simulation")
    fen_s.geometry("400x150")

    frame = Frame(fen_s)
    frame2 = Frame(frame)

    Label(frame2, text="nom de la sauvegarde: ").pack(side=LEFT)
    nom = Entry(frame2)
    nom.pack(expand=YES,side=RIGHT)
    
    frame2.pack(side=TOP)
    
    confirm = Button(frame, text='confirmer', command=partial(confirmer2, fen_s, nom, grille))
    confirm.pack(side=BOTTOM)

    frame.pack(expand=YES)
    fen_s.mainloop()
    fen_s.destroy()


file = None