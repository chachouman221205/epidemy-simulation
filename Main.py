import random
from tkinter import *
import regles as regles

def etat_suivant(L, nL, x, y, R, V):
    if type(L[y][x]) == int:
        if L[y][x] >= 2:
            nL[y][x] = L[y][x]-1
        else:
            nL[y][x] = "R"
    else:
        case_oubli(L, nL, x, y, R)
        case_mort(L, nL, x, y, R, V)
        case_contamine(L, nL, x, y, R)

def prochaine_etape(grille):
    global R, V
    x_max = len(grille[0])
    y_max = len(grille)
    nouvelle_grille = grille
    
    for y in range(y_max):
        for x in range(x_max):
            etat_suivant(grille, nouvelle_grille, x, y, R, V)

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
    if case_est_contamine(L, x, y, R):
        nL[y][x] = random.randint(R["recup_min"], R["recup_max"])

def case_est_oubli(L, x, y, R):
    if L[y][x] == "R":
        return random.random() < R["proba_oubli"]

def case_oubli(L, nL, x, y, R):
    if case_est_oubli(L, x, y, R):
        nL[y][x] = "S"

def case_est_mort(L, x, y, R, V):
    if type(L[y][x]) == int:
        return random.random()*V[y][x] < R["proba_mort"]

def case_mort(L, nL, x, y, R, V):
    if case_est_mort(L, x, y, R, V):
        nL[y][x] = "M"

def Recommencer():
    global grille,ligne
    for y in range (0,10):
        for x in range (0,10):
            can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = 'white')
            ligne.append("S")
        grille.append(ligne)
        ligne = []
        compteur.set(0)

def click(event):
    global compteur, grille, R
    x = event.x//30
    y = event.y//30
    grille[y][x] = random.randint(R["recup_min"], R["recup_max"])
    can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = 'red')
    Compter()

def infect():
    global compteur, grille
    l = random.choice(case_libre)
    x = l%10
    y = (l-x)//10
    grille[y][x] = random.randint(R["recup_min"], R["recup_max"])
    case_libre.remove(l)  
    can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = 'red')
    Compter()
    
def nouvelle_regle():
    global R 
    regles.nouvelle_regle()
    R = regles.R
    

def dessiner(grille):
    global couleurs
    for y in range (0,10):
        for x in range (0,10):
            if type(grille[y][x]) == int:
                can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = 'red')
            else:
                can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = couleurs[grille[y][x]])

def simuler():
    global grille
    print(grille)
    grille = prochaine_etape(grille)
    print(grille)
    dessiner(grille)
    Compter()
    
def Compter():
    global compteur, grille
    infectes = 0
    for y in grille:
        for x in y:
            if type(x)== int:
                infectes += 1
    compteur.set(infectes)



# Initialisation des variables

R = {"nb_voisins": 3, "recup_min": 8,"recup_max": 10, "proba_mort": 0.1, "proba_oubli": 0.1}
V = [[1 for y in range(10)] for x in range(10)] # Liste de vulnérabilité à la mort


fen1 = Tk()
fen1.title('Simulation')
fen1.geometry('450x450')
can1 = Canvas(fen1,bg='white',height=300,width=300)


case_libre = [e for e in range (0,100)]
grille = []
ligne = []
coul = 'white'
couleurs = {"M":'black',"R":"grey","S":"white"} 
compteur = IntVar(value=0)
              
bou3 = Button(fen1,text='Infection',command=infect)
bou4 = Button(fen1,text='simuler',command=simuler)

for y in range (0,10):
    for x in range (0,10):
        can1.create_rectangle(x*30,y*30,x*30+30,y*30+30,fill = coul)
        ligne.append("S")
    grille.append(ligne)
    ligne = []

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

can1.bind("<Button-1>", click)

fen1.config(menu=menubar)
bou3.pack(side=RIGHT)
bou4.pack(side=RIGHT)
Label(textvariable=compteur).pack()
can1.pack()

mainloop()