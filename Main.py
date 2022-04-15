import random
from tkinter import *
import regles 
import erreur  


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
    else:
        case_oubli(L, nL, x, y, R)
        case_contamine(L, nL, x, y, R)

def prochaine_etape(grille):
    global R, V
    x_max = len(grille[0])
    y_max = len(grille)
    nouvelle_grille = grille
    nb_mort, nb_recovered, nb_safe, nb_infecte = 0, 0, 0, 0
    
    for y in range(y_max):
        for x in range(x_max):
            etat_suivant(grille, nouvelle_grille, x, y, R, V)
            if nouvelle_grille[y][x] == 'R':
                nb_recovered += 1
            elif nouvelle_grille[y][x] == 'M':
                nb_mort += 1
            elif nouvelle_grille[y][x] == 'S':
                nb_safe += 1
            else:
                nb_infecte += 1
    historique["S"].append(nb_safe)
    historique["M"].append(nb_mort)
    historique["R"].append(nb_recovered)
    historique["I"].append(nb_infecte)
    update_labels()
    return nouvelle_grille

def n_voisins_contamine(L, x, y):
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
    return n_voisins_contamine(L, x, y)/R["nb_voisins"] > random.random() and L[y][x] == "S"

def case_contamine(L, nL, x, y, R):
    global compteur
    if case_est_contamine(L, x, y, R):
        nL[y][x] = "I"
        compteur.set(compteur.get()+1)
        case_libre.remove(y*10+x)
        

def case_est_oubli(L, x, y, R):
    if L[y][x] == "R":
        return random.random() < R["proba_oubli"]

def case_oubli(L, nL, x, y, R):
    if case_est_oubli(L, x, y, R):
        nL[y][x] = "S"
        case_libre.append(y*10+x)

def case_est_mort(L, x, y, R, V):
    if type(L[y][x]) == int:
        return random.random() < R["proba_mort"] * V[y][x]

def case_mort(L, nL, x, y, R, V):
    global compteur
    if case_est_mort(L, x, y, R, V):
        nL[y][x] = "M"
        compteur.set(compteur.get()-1)

def Recommencer():
    global compteur, historique
    grille = []
    for y in range (0,10):
        ligne = []
        for x in range (0,10):
            can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = 'white')
            ligne.append("S")
        grille.append(ligne)
        historique = {"S": [], "M": [], "I": [], "R": []}
    compteur = 0

    return grille

def click(event):
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
            erreur.erreur('Tuer','Cette personne ne peut pas être Tuer')
            
    elif mode == 1:
        if grille[y][x] != "S":
            case_libre.append(y*10+x)
            can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = 'white')
            if type(grille[y][x])==int :
                compteur.set(compteur.get()-1)
            grille[y][x] = "S"
        else :
            erreur.erreur('Soigner','Cette personne ne peut pas être Soigner')
            
    update_labels()
    
def infect():
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
    global couleurs
    for y in range (0,10):
        for x in range (0,10):
            if type(grille[y][x]) == int or grille[y][x] == "I":
                can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = 'red')
            else:
                can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = couleurs[grille[y][x]])

def simuler():
    global grille  
    grille = prochaine_etape(grille)
    dessiner(grille)

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

# Initialisation des variables

R = {"nb_voisins": 3, "recup_min": 8,"recup_max": 10, "proba_mort": 0.01, "proba_oubli": 0.1}
V = [[1 for y in range(10)] for x in range(10)] # Liste de vulnérabilité à la mort
historique = {"S": [], "M": [], "I": [], "R": []}
couleurs = {"M":'black',"R":"light grey","S":"white"} 
case_libre = [e for e in range (0,100)]  
mode = 0

fen1 = Tk()
fen1.title('Simulation')
fen1.geometry('500x500')

can1 = Canvas(fen1,bg='white',height=300,width=300)
can1.grid(row=0,column=1)

can2 = Canvas(fen1,bg='white',height=300,width=300)
can2.grid(row=0,column=2)

can3 = Canvas(fen1,bg='white',height=300,width=300)
can3.grid(row=1,column=1)

grille = Recommencer()
compteur = IntVar(value=0)
label_text = StringVar(value="Nombre d'inféctés: " + str(compteur.get()))
Label(can2,textvariable=label_text).grid(row=4,column=1, ipadx=20)

bou3 = Button(can3,text='Infection',command=infect).grid(row=3,column=2, ipadx=30, ipady=10)
bou4 = Button(can3,text='simuler',command=simuler).grid(row=4,column=2, ipadx=30, ipady=10)



can1.bind("<Button-1>", click)


menubar = Menu(fen1)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Créer", command=nouvelle_regle)
menu1.add_command(label="Editer", command=nouvelle_regle)
menu1.add_separator()
menu1.add_command(label="Quitter", command=quit)
menubar.add_cascade(label="Virus", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Réinitialiser", command=Recommencer)
menu2.add_command(label="Modifier", command=nouvelle_regle)
menubar.add_cascade(label="Affichage", menu=menu2)

menu3 = Menu(menubar, tearoff=0)
menu3.add_command(label="Contaminer", command=mode_contaminer)
menu3.add_command(label="Tuer", command=mode_tuer)
menu3.add_command(label="Soigner", command=mode_soigner)
menu3.add_command(label="Vacciner", command=mode_vacciner)
menubar.add_cascade(label="Pointeur", menu=menu3)

fen1.config(menu=menubar)

mainloop()
