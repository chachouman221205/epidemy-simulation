import random
from tkinter import *
import regles 
import erreur  
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
    else:
        case_oubli(L, nL, x, y, R)
        case_contamine(L, nL, x, y, R)

def prochaine_etape(grille):
    """
    Met à jour la grille et l'historique avec les données de la nouvelle liste
    """
    global R, V
    x_max = len(grille[0])
    y_max = len(grille)
    nouvelle_grille = grille
    nb_mort, nb_recovered, nb_safe, nb_infecte, nb_vaccine = 0, 0, 0, 0, 0
    case_vaccine(grille, nouvelle_grille, R)
    
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
    """
    Renvoie le nombre de voisins infectés à côté d'une case de coordonnées (x,y)
    """
    nb_voisins = 0
    for change_x in range(-1, 2):
        for change_y in range(-1, 2):
            if 0 <= x + change_x < len(L) and 0 <= y + change_y < len(L):
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
    global compteur
    if case_est_contamine(L, x, y, R):
        nL[y][x] = "I"
        compteur.set(compteur.get()+1)
        case_libre.remove(y*10+x)
        

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
    if case_est_oubli(L, x, y, R):
        nL[y][x] = "S"
        case_libre.append(y*10+x)

def case_est_mort(L, x, y, R, V):
    """
    Renvoie un booléen indiquant si la case de coordonnées (x,y) peut être tuée
    """
    if type(L[y][x]) == int:
        return random.random() < R["proba_mort"] * V[y][x]

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
    if flag_vaccination and random.random() < R["proba_vaccination"]:
        x, y = random.randint(0, 9), random.randint(0, 9)
        while L[y][x] != "S" and L[y][x] != "R":
            x, y = random.randint(0, 9), random.randint(0, 9)
        nL[y][x] = "V"

def vaccine():
    """
    Vaccine une case au hasard si possible
    """
    global compteur, grille, flag_vaccination
    if len(case_libre) > 0 and flag_vaccination and random.random() < R["proba_vaccination"]:
        l = random.choice(case_libre)
        x = l%10
        y = l//10
        grille[y][x] = "V"
        case_libre.remove(l)
        can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = 'blue')
        update_labels()
    elif not flag_vaccination:
        flag_vaccination = True

def Recommencer():
    """
    Renitialise la grille de propagation
    """
    global historique, grille, compteur, case_libre
    grille = []
    case_libre = [e for e in range (0,100)] 
    for y in range (0,10):
        ligne = []
        for x in range (0,10):
            can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = 'white')
            ligne.append("S")
        grille.append(ligne)
        historique = {"S": [], "M": [], "I": [], "R": [], "V": []}
    compteur.set(0)
    update_labels()

    return grille

def click(event):
    """
    Permet de cliquer sur une case pour en modifier l'état
    """
    global compteur, grille, R, mode
    x = event.x//30
    y = event.y//30
    
    if mode == 0:
        if grille[y][x] == 'S':
            grille[y][x] = random.randint(R["recup_min"], R["recup_max"])
            can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = 'red')
            compteur.set(compteur.get()+1)
            case_libre.remove(y*10+x)
        else :
            erreur.erreur('Infection','Cette personne ne peut pas être infectée')
            
    elif mode == -1:
        if grille[y][x] != "M":
            can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = 'black')
            if type(grille[y][x])==int:
                compteur.set(compteur.get()-1)
            elif grille[y][x] == "S":
                case_libre.remove(y*10+x)
            grille[y][x] = "M"
        else :
            erreur.erreur('Tuer','Cette personne ne peut pas être Tuée')
            
    elif mode == 1:
        if grille[y][x] != "S":
            case_libre.append(y*10+x)
            can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = 'white')
            if type(grille[y][x])==int :
                compteur.set(compteur.get()-1)
            grille[y][x] = "S"
        else :
            erreur.erreur('Soigner','Cette personne ne peut pas être Soignée')
    elif mode == 2:
        if grille[y][x] != "V":
            can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = 'blue')
            if type(grille[y][x])==int :
                compteur.set(compteur.get()-1)
            elif grille[y][x] == "S":
                case_libre.remove(y*10+x)
            grille[y][x] = "V"
        else :
            erreur.erreur('Vacciner','Cette personne ne peut pas être Vaccinée')
    update_labels()
    
def infect():
    """
    Infecte une case au hasard
    """
    global compteur, grille
    if len(case_libre) > 0:
        l = random.choice(case_libre)
        x = l%10
        y = (l-x)//10
        grille[y][x] = random.randint(R["recup_min"], R["recup_max"])
        case_libre.remove(l)  
        can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = 'red')
        compteur.set(compteur.get()+1)
        update_labels()
    else:
        erreur.erreur('Infection','Aucune case ne peut être infectée')
    
def nouvelle_regle():
    global R 
    regles.nouvelle_regle()
    R = regles.R

def dessiner(grille):
    """
    Affiche la grille sur Tkinter
    """
    can1.delete("all")
    global couleurs
    for y in range (0,10):
        for x in range (0,10):
            if type(grille[y][x]) == int or grille[y][x] == "I":
                can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = 'red')
            else:
                can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = couleurs[grille[y][x]])

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
        fen1.after(10, simuler)
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

def afficher_graphique():
    """
    Affiche le graphe de la progression de la propagation depuis le début
    """
    global historique
    histo2 = {"I":[],"M":[],"R":[],"S":[]}

    axe_x = list(range(len(historique["I"])))
    
    for i in axe_x:
        histo2["M"].append(historique["M"][i])
        histo2["R"].append(histo2["M"][-1] + historique["R"][i])
        histo2["I"].append(histo2["R"][-1] + historique["I"][i])
        histo2["S"].append(histo2["I"][-1] + historique["S"][i])
        
        plt.axes().set_facecolor("0.15")
        plt.fill_between(axe_x, histo2["I"], histo2["S"], color = "white")
        plt.fill_between(axe_x, histo2["R"], histo2["I"], color = "red")
        plt.fill_between(axe_x, histo2["M"], histo2["R"], color = "grey")
        plt.fill_between(axe_x, histo2["M"], [0 for x in axe_x], color ="black")
        plt.show()

def panneau_control():
    global fen2, can3
    fen2 = Tk()
    fen2.title('Panneau_control')
    fen2.geometry('500x500')
    
    can3 = Canvas(fen2,bg='white',height=300,width=300)
    can3.grid(row=1,column=1)
    
    bou3 = Button(can3,text='Infection',command=infect).grid(row=0,column=2, ipadx=30, ipady=10)
    bou4 = Button(can3,text='simuler',command=simuler).grid(row=0,column=3, ipadx=30, ipady=10)
    bou5 = Button(can3,text='pause',command=stop_simuler).grid(row=0,column=1, ipadx=30, ipady=10)
    bou6 = Button(can3,text='Vacciner',command=vaccine).grid(row=0,column=4, ipadx=30, ipady=10)

# Initialisation des variables

R = {"nb_voisins": 3, "recup_min": 8,"recup_max": 10, "proba_mort": 0.01, "proba_oubli": 0.1, "proba_vaccination": 0.1}
V = [[1 for y in range(10)] for x in range(10)] # Liste de vulnérabilité à la mort
historique = {"S": [], "M": [], "I": [], "R": [], "V": []}
couleurs = {"M":'black',"R":"light grey","S":"white","V":"blue"} 
case_libre = [e for e in range (0,100)]  
mode = 0
flag = True
flag_vaccination = False

fen1 = Tk()
fen1.title('Simulation')
fen1.geometry('500x500')

can1 = Canvas(fen1,bg='white',height=300,width=300)
can1.grid(row=0,column=1)

can2 = Canvas(fen1,bg='white',height=300,width=300)
can2.grid(row=0,column=2)

can4 = Canvas(fen1,bg='white',height=300,width=300)
can4.grid(row=1,column=1)

compteur = IntVar(value=0)
label_text = StringVar(value="Nombre d'inféctés: " + str(compteur.get()))
Label(can2,textvariable=label_text).grid(row=4,column=1, ipadx=30)

label_text2 = StringVar(value="Nombre d'inféctés: " + str(0))
Label(can2,textvariable=label_text2).grid(row=5,column=1, ipadx=30)

label_text3 = StringVar(value="Nombre de vaccinés: " + str(0))
Label(can2,textvariable=label_text3).grid(row=6,column=1, ipadx=30)

bou1 = Button(can4,text='Infection',command=panneau_control).grid(row=0,column=2, ipadx=30, ipady=10)

grille = Recommencer()

can1.bind("<Button-1>", click)


menubar = Menu(fen1)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Créer", command=nouvelle_regle)
menu1.add_command(label="Editer", command=nouvelle_regle)
menu1.add_separator()
menu1.add_command(label="Quitter", command=quit)
menubar.add_cascade(label="Virus", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Modifier", command=nouvelle_regle)
menu2.add_command(label="Afficher le graphique", command=afficher_graphique)
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
