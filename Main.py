import random
from tkinter import *
import regles, erreur
import taille as T
import matplotlib.pyplot as plt

def etat_suivant(L, nL, x, y, R, V):
    """
    Génère la liste contenant le statut de la case de coordonnées (x,y) mis à jour 
    """
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
    global R, V, taille
    """
    Met à jour la grille et l'historique avec les données de la nouvelle liste
    """
    nouvelle_grille = grille
    nb_mort, nb_recovered, nb_safe, nb_infecte, nb_vaccine = 0, 0, 0, 0, 0
    
    vaccine()
    
    for y in range(taille[1]):
        for x in range(taille[0]):
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
    """
    Renvoie le nombre de voisins infectés à côté d'une case de coordonnées (x,y)
    """
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
    """
    Renvoie un booléen indiquant si la case de coordonnées (x,y) peut être contaminée
    """
    return n_voisins_contamine(L, x, y)/R["nb_voisins"] > random.random() and L[y][x] == "S"
def case_contamine(L, nL, x, y, R):
    """
    Met à jour la case de coordonnées (x,y) par rapport à si elle est contaminée ou pas
    """
    global compteur, taille
    if case_est_contamine(L, x, y, R):
        nL[y][x] = "I"
        compteur.set(compteur.get()+1)
        case_libre.remove(y*taille[0]+x)

def case_est_oubli(L, x, y, R):
    """
    Renvoie un booléen indiquant si la case de coordonnées (x,y) peut perdre son immunité temporaire à l'infection
    """
    if L[y][x] == "R":
        return random.random() < R["proba_oubli"]
def case_oubli(L, nL, x, y, R):
    """
    Met à jour la case de coordonnées (x,y) par rapport à si elle est pert son immunité temporaire à l'infection ou pas
    """
    global taille
    if case_est_oubli(L, x, y, R):
        nL[y][x] = "S"
        case_libre.append(y*taille[0]+x)

def case_est_mort(L, x, y, R, V):
    """
    Renvoie un booléen indiquant si la case de coordonnées (x,y) peut être tuée
    """
    if type(L[y][x]) == int:
        return random.random() < R["proba_mort"] * V[y][x]
    return False
def case_mort(L, nL, x, y, R, V):
    """
    Met à jour la case de coordonnées (x,y) par rapport à si elle est morte ou pas
    """
    global compteur
    if case_est_mort(L, x, y, R, V):
        nL[y][x] = "M"
        compteur.set(compteur.get()-1)

def case_vaccine(L, nL, R):
    """
    Met à jour la case de coordonnées (x,y) par rapport à si elle est vaccinée ou pas
    """
    global flag_vaccination, taille
    if flag_vaccination and random.random() < R["proba_vaccination"]:
        x, y = random.randint(0, taille[0]), random.randint(0, taille[1])
        while L[y][x] != "S" and L[y][x] != "R":
            x, y = random.randint(0, taille[0]), random.randint(0, taille[1])
        nL[y][x] = "V"

def vaccine():
    """
    Vaccine une case au hasard si possible
    """
    global compteur, grille, flag_vaccination, taille
    if len(case_libre) > 0 and flag_vaccination and random.random() < R["proba_vaccination"]:
        l = random.choice(case_libre)
        x = l%taille[0]
        y = l//taille[0]
        grille[y][x] = "V"
        case_libre.remove(l)
        update_labels()
        dessiner(grille)
    elif not flag_vaccination:
        flag_vaccination = True

def Recommencer(taille_=None):
    if taille_ == None:
        global taille
        taille_ = taille
    print("Nouvelle simulation:")
    print("- taille:", taille)
    
    global historique, grille, compteur, case_libre, V
    grille = []
    case_libre = list(range(taille_[0]*taille_[1]))
    V = [[1 for x in range(taille_[0])] for y in range(taille_[1])]
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
    """
    Permet de cliquer sur une case pour en modifier l'état
    """
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
    """
    Infecte une case au hasard
    """
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
    Recommencer(taille)

def dessiner(grille):
    """
    Affiche la grille sur Tkinter
    """
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
    """
    Met à jour constamment la grille tout en l'affichant jusqu'à que la fonction stop_simuler soit appelée (ligne 241)
    """
    global grille, flag, compteur
    grille = prochaine_etape(grille)
    dessiner(grille)
    if flag:
        if compteur.get() == 0:
            return
        fen1.after(1000//vitesse.get()**2-10, simuler)
    else:
        flag = True
def stop_simuler():
    """
    Arrête la simulation
    """
    global flag
    flag = False

def update_labels():
    """
    Affiche le nombre des différents états
    """
    global compteur, label_text, label_text2
    label_text.set("Nombre d'infectés: " + str(compteur.get()))
    
    if len(historique["M"])==0:
        label_text2.set("Nombre de morts: " + str(0))
    else:
        label_text2.set("Nombre de morts: " + str(historique["M"][-1]))
        
    if len(historique["M"])==0:
            label_text3.set("Nombre de vaccinés: " + str(0))
    else:
        label_text3.set("Nombre de vaccinés: " + str(historique["V"][-1]))

# Les fonctions si dessous modifient l'état du click pour modifier l'état des cases
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
    """
    Affiche le graphe de la progression de la propagation depuis le début
    """
    global historique
    histo2 = {"I":[],"M":[],"R":[],"S":[],"V":[]}

    axe_x = list(range(len(historique["I"])))
    
    for x in axe_x:
        histo2["M"].append(historique["M"][x])
        histo2["R"].append(histo2["M"][-1] + historique["R"][x])
        histo2["I"].append(histo2["R"][-1] + historique["I"][x])
        histo2["S"].append(histo2["I"][-1] + historique["S"][x])
        histo2["V"].append(histo2["S"][-1] + historique["V"][x])

    plt.axes().set_facecolor("0.15")
    plt.fill_between(axe_x, histo2["S"], histo2["V"], color = "blue")
    plt.fill_between(axe_x, histo2["I"], histo2["S"], color = "white")
    plt.fill_between(axe_x, histo2["R"], histo2["I"], color = "red")
    plt.fill_between(axe_x, histo2["M"], histo2["R"], color = "grey")
    plt.fill_between(axe_x, histo2["M"], [0 for x in axe_x], color ="black")
    plt.show()

def afficher_graphique2():
    global historique
    histo2 = {"I":[], "S":[], "R":[], "V":[]}
    axe_x = list(range(len(historique["I"])))

    for x in axe_x:
        total = historique["I"][x] + historique["S"][x] + historique["R"][x] + historique["V"][x]

        histo2["I"].append(historique["I"][x]/total)
        histo2["S"].append(historique["S"][x]/total +histo2["I"][-1])
        histo2["R"].append(historique["R"][x]/total +histo2["S"][-1])
        histo2["V"].append(historique["V"][x]/total +histo2["R"][-1])

    plt.axes().set_facecolor("0.15")
    plt.fill_between(axe_x, histo2["V"], histo2["R"], color="blue")
    plt.fill_between(axe_x, histo2["R"], histo2["S"], color="grey")
    plt.fill_between(axe_x, histo2["S"], histo2["I"], color="white")
    plt.fill_between(axe_x, histo2["I"], [0 for x in axe_x], color="red")
    plt.show()

def panneau_control():
    global fen2, can3, vitesse
    fen2 = Tk()
    fen2.title('Panneau_control')
    fen2.geometry('450x100')
    
    can3 = Canvas(fen2,bg='white',height=300,width=300)
    can3.grid(row=1,column=1)
    
    bou3 = Button(can3,text='Infection',command=infect).grid(row=0,column=2, ipadx=30, ipady=10)
    bou4 = Button(can3,text='simuler',command=simuler).grid(row=0,column=3, ipadx=30, ipady=10)
    bou5 = Button(can3,text='pause',command=stop_simuler).grid(row=0,column=1, ipadx=30, ipady=10)
    bou6 = Button(can3,text='Vacciner',command=vaccine).grid(row=0,column=4, ipadx=30, ipady=10)

    vitesse = Scale(can3,label="Vitesse de simulation",orient='horizontal',from_=1,to=10,tickinterval=0.1)
    vitesse.grid(row=1,column=1,columnspan=4,ipadx=170,ipady=10)

# Initialisation des variables


R = {"nb_voisins": 3, "recup_min": 8,"recup_max": 10, "proba_mort": 0.01, "proba_oubli": 0.1, "proba_vaccination": 0.1}

taille = (25, 25)
V = [] # Liste de vulnérabilité à la mort
historique = {}
couleurs = {"M":'black',"R":"light grey","S":"white","V":"blue"} 
case_libre = []
mode = 0
flag = True
taille_cellule = 500//max(taille)
flag_vaccination = False

# création de la fenêtre

fen1 = Tk()
fen1.title('Simulation')
fen1.geometry('700x600')

#création des différents canvas

can1 = Canvas(fen1,bg='white',height=500,width=500)
can1.grid(row=0,column=1)
can2 = Canvas(fen1,bg='white',height=300,width=300)
can2.grid(row=0,column=2)
can4 = Canvas(fen1,bg='white',height=300,width=300)
can4.grid(row=1,column=1)

#création des compteurs

compteur = IntVar(value=0)
label_text = StringVar(value="Nombre d'inféctés: " + str(compteur.get()))
Label(can2,textvariable=label_text).grid(row=4,column=1, ipadx=30)
label_text2 = StringVar(value="Nombre d'inféctés: " + str(0))
Label(can2,textvariable=label_text2).grid(row=5,column=1, ipadx=30)
label_text3 = StringVar(value="Nombre de vaccinés: " + str(0))
Label(can2,textvariable=label_text3).grid(row=6,column=1, ipadx=30)

bou1 = Button(can4,text='Panneau de contrôle',command=panneau_control).grid(row=0,column=2, ipadx=30, ipady=10)

grille = Recommencer()

can1.bind("<Button-1>", click)

#création de la barre de menu

menubar = Menu(fen1)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Créer", command=nouvelle_regle)
menu1.add_command(label="Editer", command=nouvelle_regle)
menu1.add_separator()
menu1.add_command(label="Quitter", command=quit)
menubar.add_cascade(label="Virus", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Modifier", command=nouvelle_regle)
menu2.add_command(label="Afficher le graphique 1", command=afficher_graphique1)
menu2.add_command(label="Afficher le graphique 2", command=afficher_graphique2)
menu2.add_command(label="Réinitialiser", command=Recommencer)
menu2.add_command(label="Taille", command=nouvelle_taille)
menubar.add_cascade(label="Affichage", menu=menu2)

menu3 = Menu(menubar, tearoff=0)
menu3.add_command(label="Contaminer", command=mode_contaminer)
menu3.add_command(label="Tuer", command=mode_tuer)
menu3.add_command(label="Soigner", command=mode_soigner)
menu3.add_command(label="Vacciner", command=mode_vacciner)
menubar.add_cascade(label="Pointeur", menu=menu3)

fen1.config(menu=menubar)

grille = Recommencer()
mainloop()
