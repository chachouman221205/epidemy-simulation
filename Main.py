import random
from tkinter import *
import regles, erreur
import taille as T
import matplotlib.pyplot as plt

def etat_suivant(L, nL, x, y, R, V):
    if type(L[y][x]) == int:
        if L[y][x] >= 2:
            nL[y][x] = L[y][x]-1
            case_mort(L, nL, x, y, R, V)
        else:
            nL[y][x] = "R"
            compteur.set(compteur.get()-1)
    elif L[y][x] == "I":
        L[y][x] = random.randint(R["recup_min"], R["recup_max"])
    elif L[y][x] == "R":
        case_oubli(L, nL, x, y, R)
    elif L[y][x] == "S":
        case_contamine(L, nL, x, y, R)

def prochaine_etape(grille):
    global R, V
    x_max = len(grille[0])
    y_max = len(grille)
    nouvelle_grille = grille
    nb_mort, nb_recovered, nb_safe, nb_infecte, nb_vaccine = 0, 0, 0, 0, 0
    
    for y in range(y_max):
        for x in range(x_max):
            etat_suivant(grille, nouvelle_grille, x, y, R, V)
            if nouvelle_grille[y][x] == 'R':
                nb_recovered += 1
            elif nouvelle_grille[y][x] == 'M':
                nb_mort += 1
            elif nouvelle_grille[y][x] == 'S':
                nb_safe += 1
            elif nouvelle_grille[y][x] == 'V':
                nb_vaccine += 1
            else:
                nb_infecte += 1
    historique["S"].append(nb_safe)
    historique["M"].append(nb_mort)
    historique["R"].append(nb_recovered)
    historique["I"].append(nb_infecte)
    historique["V"].append(nb_vaccine)
    update_labels()
    return nouvelle_grille

def n_voisins_contamine(L, x, y):
    nb_voisins = 0
    for change_x in range(-1, 2):
        for change_y in range(-1, 2):
            if 0 <= x + change_x < len(L[0]) and 0 <= y + change_y < len(L):
                if type(L[y + change_y][x + change_x]) == int:
                    nb_voisins += 1
    if type(L[y][x]) == int:
        nb_voisins -= 1
    return nb_voisins

def case_est_contamine(L, x, y, R):
    return n_voisins_contamine(L, x, y)/R["nb_voisins"] > random.random() and L[y][x] == "S"
def case_contamine(L, nL, x, y, R):
    global compteur, taille
    if case_est_contamine(L, x, y, R):
        nL[y][x] = "I"
        compteur.set(compteur.get()+1)
        case_libre.remove(y*taille[0]+x)

def case_est_oubli(L, x, y, R):
    if L[y][x] == "R":
        return random.random() < R["proba_oubli"]
def case_oubli(L, nL, x, y, R):
    global taille
    if case_est_oubli(L, x, y, R):
        nL[y][x] = "S"
        case_libre.append(y*taille[0]+x)

def case_est_mort(L, x, y, R, V):
    if type(L[y][x]) == int:
        return random.random() < R["proba_mort"] * V[y][x]
    return False
def case_mort(L, nL, x, y, R, V):
    global compteur
    if case_est_mort(L, x, y, R, V):
        nL[y][x] = "M"
        compteur.set(compteur.get()-1)

def Recommencer(taille_=None):
    if taille_ == None:
        global taille
        taille_ = taille
    print(taille)
    
    global historique, grille, compteur, case_libre, V
    grille = []
    case_libre = list(range(taille_[0]*taille_[1]))
    V = [[1 for y in range(taille_[1])] for x in range(taille_[0])]
    for y in range(taille_[1]):
        ligne = []
        for x in range(taille_[0]):
            ligne.append("S")
        grille.append(ligne)
    historique = {"S": [], "M": [], "I": [], "R": [], "V": []}
    compteur.set(0)
    update_labels()
    dessiner(grille)
    return grille

def click(event):
    global compteur, grille, R, mode, taille_cellule
    x = event.x//taille_cellule
    y = event.y//taille_cellule
    
    if mode == 0:
        if grille[y][x] == 'S':
            grille[y][x] = random.randint(R["recup_min"], R["recup_max"])
            can1.create_rectangle(x*taille_cellule,y*taille_cellule,x*taille_cellule+taille_cellule,y*taille_cellule+taille_cellule,fill = 'red', width = 0)
            compteur.set(compteur.get()+1)
            case_libre.remove(y*taille[0]+x)
        else :
            erreur.erreur('Infection','Cette personne ne peut pas être infectée')
            
    elif mode == -1:
        if grille[y][x] != "M":
            can1.create_rectangle(x*taille_cellule,y*taille_cellule,x*taille_cellule+taille_cellule,y*taille_cellule+taille_cellule,fill = 'black', width = 0)
            if type(grille[y][x])==int:
                compteur.set(compteur.get()-1)
            elif grille[y][x] == "S":
                case_libre.remove(y*taille[0]+x)
            grille[y][x] = "M"
        else :
            erreur.erreur('Tuer','Cette personne ne peut pas être Tuée')
            
    elif mode == 1:
        if grille[y][x] != "S":
            case_libre.append(y*taille[0]+x)
            can1.create_rectangle(x*taille_cellule,y*taille_cellule,x*taille_cellule+taille_cellule,y*taille_cellule+taille_cellule,fill = 'white', width = 0)
            if type(grille[y][x])==int :
                compteur.set(compteur.get()-1)
            grille[y][x] = "S"
        else :
            erreur.erreur('Soigner','Cette personne ne peut pas être Soignée')
    elif mode == 2:
        if grille[y][x] != "V":
            can1.create_rectangle(x*taille_cellule,y*taille_cellule,x*taille_cellule+taille_cellule,y*taille_cellule+taille_cellule,fill = 'blue', width = 0)
            if type(grille[y][x])==int :
                compteur.set(compteur.get()-1)
            elif grille[y][x] == "S":
                case_libre.remove(y*taille[0]+x)
            grille[y][x] = "V"
        else :
            erreur.erreur('Vacciner','Cette personne ne peut pas être Vaccinée')
    update_labels()
    
def infect():
    global compteur, grille, taille_cellule
    if len(case_libre) > 0:
        l = random.choice(case_libre)
        x = l%taille[1]
        y = l//taille[1]
        grille[y][x] = random.randint(R["recup_min"], R["recup_max"])
        case_libre.remove(l)  
        can1.create_rectangle(x*taille_cellule,y*taille_cellule,x*taille_cellule+taille_cellule,y*taille_cellule+taille_cellule,fill = 'red', width = 0)
        compteur.set(compteur.get()+1)
        update_labels()
    else:
        erreur.erreur('Infection','Aucune case ne peut être infectée')
    
def nouvelle_regle():
    global R 
    regles.nouvelle_regle()
    R = regles.R

def nouvelle_taille():
    global taille, taille_cellule
    T.nouvelle_taille()
    taille = (T.x, T.y)
    taille_cellule = 500//max(taille)
    print(taille)
    Recommencer(taille)

def dessiner(grille):
    can1.delete("all")
    global couleurs, taille, taille_cellule
    if taille_cellule <= 5:
        outline = 0
    else:
        outline = 1
    for y in range(taille[1]):
        for x in range(taille[0]):
            if type(grille[y][x]) == int or grille[y][x] == "I":
                can1.create_rectangle(x*taille_cellule,y*taille_cellule,x*taille_cellule+taille_cellule,y*taille_cellule+taille_cellule, fill='red', width = 0)
            else:
                can1.create_rectangle(x*taille_cellule,y*taille_cellule,x*taille_cellule+taille_cellule,y*taille_cellule+taille_cellule, fill=couleurs[grille[y][x]], width = 0)

def simuler():
    global grille, flag, compteur
    grille = prochaine_etape(grille)
    dessiner(grille)
    if flag:
        if compteur.get() == 0:
            return
        fen1.after(10, simuler)
    else:
        flag = True
def stop_simuler():
    global flag
    flag = False

def update_labels():
    global compteur, label_text
    label_text.set("Nombre d'infectés: " + str(compteur.get()))   
    
def mode_tuer():
    global mode
    mode = -1
def mode_contaminer():
    global mode
    mode = 0
def mode_soigner():
    global mode
    mode = 1
def mode_vacciner():
    global mode
    mode = 2

def afficher_graphique1():
    global historique
    histo2 = {"I":[],"M":[],"R":[],"S":[]}

    axe_x = list(range(len(historique["I"])))
    
    for x in axe_x:
        histo2["M"].append(historique["M"][x])
        histo2["R"].append(histo2["M"][-1] + historique["R"][x])
        histo2["I"].append(histo2["R"][-1] + historique["I"][x])
        histo2["S"].append(histo2["I"][-1] + historique["S"][x])

    plt.axes().set_facecolor("0.15")
    plt.fill_between(axe_x, histo2["I"], histo2["S"], color = "white")
    plt.fill_between(axe_x, histo2["R"], histo2["I"], color = "red")
    plt.fill_between(axe_x, histo2["M"], histo2["R"], color = "grey")
    plt.fill_between(axe_x, histo2["M"], [0 for x in axe_x], color ="black")
    plt.show()

def afficher_graphique2():
    global historique
    histo2 = {"I":[], "S":[], "R":[]}
    axe_x = list(range(len(historique["I"])))

    for x in axe_x:
        total = historique["I"][x] + historique["S"][x] + historique["R"][x]

        histo2["I"].append(historique["I"][x]/total)
        histo2["S"].append(historique["S"][x]/total +histo2["I"][-1])
        histo2["R"].append(historique["R"][x]/total +histo2["S"][-1])

    plt.axes().set_facecolor("0.15")
    plt.fill_between(axe_x, histo2["R"], histo2["S"], color="grey")
    plt.fill_between(axe_x, histo2["S"], histo2["I"], color="white")
    plt.fill_between(axe_x, histo2["I"], [0 for x in axe_x], color="red")
    plt.show()

# Initialisation des variables

R = {"nb_voisins": 3, "recup_min": 8,"recup_max": 10, "proba_mort": 0.01, "proba_oubli": 0.1}

taille = (50, 50)
V = [] # Liste de vulnérabilité à la mort
historique = {}
couleurs = {"M":'black',"R":"light grey","S":"white","V":"blue"} 
case_libre = []
mode = 0
flag = True
taille_cellule = 500//max(taille)

fen1 = Tk()
fen1.title('Simulation')
fen1.geometry('1000x600')

can1 = Canvas(fen1,bg='white',height=500,width=500)
can1.grid(row=0,column=1)

can2 = Canvas(fen1,bg='white',height=300,width=300)
can2.grid(row=0,column=2)

can3 = Canvas(fen1,bg='white',height=300,width=300)
can3.grid(row=1,column=1)


compteur = IntVar(value=0)
label_text = StringVar(value="Nombre d'inféctés: " + str(compteur.get()))
Label(can2,textvariable=label_text).grid(row=4,column=1, ipadx=20)

grille = Recommencer(taille)

bou3 = Button(can3,text='Infection',command=infect).grid(row=0,column=2, ipadx=30, ipady=10)
bou4 = Button(can3,text='simuler',command=simuler).grid(row=0,column=3, ipadx=30, ipady=10)
bou5 = Button(can3,text='pause',command=stop_simuler).grid(row=0,column=1, ipadx=30, ipady=10)


can1.bind("<Button-1>", click)


menubar = Menu(fen1)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Créer", command=nouvelle_regle)
menu1.add_command(label="Editer", command=nouvelle_regle)
menu1.add_separator()
menu1.add_command(label="Quitter", command=fen1.destroy)
menubar.add_cascade(label="Virus", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Modifier", command=nouvelle_regle)
menu2.add_command(label="Taille", command=nouvelle_taille)
menu2.add_command(label="Afficher le graphique", command=afficher_graphique2)
menu2.add_command(label="Réinitialiser", command=Recommencer)
menubar.add_cascade(label="Affichage", menu=menu2)

menu3 = Menu(menubar, tearoff=0)
menu3.add_command(label="Contaminer", command=mode_contaminer)
menu3.add_command(label="Tuer", command=mode_tuer)
menu3.add_command(label="Soigner", command=mode_soigner)
menu3.add_command(label="Vacciner", command=mode_vacciner)
menubar.add_cascade(label="Pointeur", menu=menu3)

fen1.config(menu=menubar)

mainloop()
